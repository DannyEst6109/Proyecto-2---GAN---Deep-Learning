"""Entrenar: python -m dragon_gan.train --help."""

import argparse
import csv
import json
import math
import os
import platform
import random
import time
from pathlib import Path

os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG', ':4096:8')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision.utils import save_image

from .data import DragonDataset
from .models import build_models


HYPOTHESES = {
    'base': 'Referencia: DCGAN con pérdida no saturante y sin ruido de entrada en D.',
    'loss': ('Creemos que la pérdida no saturante de la base mejorará el aprendizaje inicial '
             'frente a minimax porque mantiene una señal útil cuando D rechaza las muestras. '
             'Lo consideraremos útil si mejora reconocimiento sin reducir diversidad con ruido fijo.'),
    'stabilization': ('Creemos que la técnica de estabilización declarada en la configuración '
                      'mejorará la estabilidad porque limita el dominio de D. Lo consideraremos útil si '
                      'reduce ese dominio conservando diversidad y coherencia con ruido fijo.'),
}
# Las configuraciones v2 no declaran el cambio de estabilización: conservan ruido 0.05 en D.
DEFAULT_STABILIZATION = {'discriminator_input_noise_std': 0.05}


def variant_config(config, experiment):
    """Configuración efectiva: cada variante cambia un solo factor respecto de la base."""
    config = dict(config)
    if experiment == 'loss':
        config['generator_loss'] = 'minimax'
    elif experiment == 'stabilization':
        change = config.get('stabilization_change', DEFAULT_STABILIZATION)
        if len(change) != 1:
            raise ValueError('stabilization_change debe modificar exactamente un parámetro.')
        config.update(change)
    elif experiment != 'base':
        raise ValueError('Experimento desconocido.')
    return config


def seed_everything(seed, threads):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.set_num_threads(threads)
    # warn_only: en CUDA algunas operaciones no tienen versión determinista y no deben abortar.
    torch.use_deterministic_algorithms(True, warn_only=True)
    torch.backends.cudnn.benchmark = False


def rng_state(loader_rng, input_noise_rng, augment_rng):
    state = np.random.get_state()
    return {'python': random.getstate(), 'numpy': (state[0], state[1].tolist(), *state[2:]),
            'torch': torch.get_rng_state(), 'loader': loader_rng.get_state(),
            'input_noise': input_noise_rng.get_state(), 'augment': augment_rng.get_state(),
            'cuda': torch.cuda.get_rng_state_all() if torch.cuda.is_available() else []}


def restore_rng(state, loader_rng, input_noise_rng, augment_rng):
    random.setstate(state['python'])
    numpy_state = state['numpy']
    np.random.set_state((numpy_state[0], np.array(numpy_state[1], dtype=np.uint32), *numpy_state[2:]))
    torch.set_rng_state(state['torch'])
    loader_rng.set_state(state['loader'])
    if 'input_noise' in state:
        input_noise_rng.set_state(state['input_noise'])
    if 'augment' in state:
        augment_rng.set_state(state['augment'])
    if state['cuda']:
        torch.cuda.set_rng_state_all(state['cuda'])


def generator_loss(logits, kind):
    if kind == 'non_saturating':
        return F.softplus(-logits).mean()  # -log(sigmoid(logit))
    if kind == 'minimax':
        return -F.softplus(logits).mean()  # log(1 - sigmoid(logit))
    raise ValueError(f'Pérdida desconocida: {kind}')


def add_noise(images, std, generator):
    if not std:
        return images
    noise = torch.randn(images.shape, dtype=images.dtype, device=images.device, generator=generator)
    return images + std * noise


def horizontal_flip(images, generator):
    """Voltea horizontalmente la mitad (aleatoria) del lote; los dragones no tienen lado preferido."""
    mask = torch.rand(len(images), generator=generator) < 0.5
    return torch.where(mask.to(images.device).view(-1, 1, 1, 1), images.flip(3), images)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def atomic_save(value, path):
    temporary = path.with_suffix('.tmp')
    torch.save(value, temporary)
    for attempt in range(5):
        try:
            temporary.replace(path)
            return
        except PermissionError:
            if os.name != 'nt' or attempt == 4:
                raise
            time.sleep(0.2 * (2 ** attempt))


def save_grid(generator, fixed_noise, path):
    was_training = generator.training
    generator.eval()
    with torch.no_grad():
        images = generator(fixed_noise)
        save_image(images, path, nrow=math.ceil(math.sqrt(len(images))),
                   normalize=True, value_range=(-1, 1))
    generator.train(was_training)


def save_history(history, folder):
    fields = ['epoch', 'loss_g', 'loss_d', 'd_real', 'd_fake', 'seconds', 'images_seen']
    with (folder / 'losses.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(history)
    figure, axis = plt.subplots(figsize=(8, 4))
    for key, label in [('loss_g', 'Generador'), ('loss_d', 'Discriminador')]:
        axis.plot([r['epoch'] for r in history], [r[key] for r in history], label=label)
    axis.set(xlabel='Época', ylabel='Pérdida media', title='Pérdidas: interpretar junto con las muestras')
    axis.legend()
    figure.tight_layout()
    figure.savefig(folder / 'losses.png', dpi=160)
    plt.close(figure)


def train(config, dataset_path, output, experiment='base', device='auto', resume=None,
          hypothesis=None, stop_after=None):
    if experiment not in HYPOTHESES:
        raise ValueError('Experimento desconocido.')
    if (config['generator_loss'] != 'non_saturating' or config['discriminator_input_noise_std'] != 0
            or config.get('discriminator_spectral_norm', False)):
        raise ValueError('La base debe ser no saturante, sin ruido ni normalización espectral; '
                         'las variantes cambian un solo factor.')
    config = variant_config(config, experiment)
    if config['image_size'] != 64 or config['channels'] != 3:
        raise ValueError('Esta arquitectura requiere imágenes RGB de 64×64.')
    for key in ('batch_size', 'epochs', 'latent_dim', 'features', 'threads', 'fixed_noise_count'):
        if not isinstance(config[key], int) or config[key] < 1:
            raise ValueError(f'{key} debe ser un entero positivo.')
    checkpoint_every = config.get('checkpoint_every', 1)
    snapshot_every = config.get('snapshot_every', 0)
    if not isinstance(checkpoint_every, int) or checkpoint_every < 1:
        raise ValueError('checkpoint_every debe ser un entero positivo.')
    if not isinstance(snapshot_every, int) or snapshot_every < 0:
        raise ValueError('snapshot_every debe ser un entero no negativo.')
    if config['batch_size'] < 2:
        raise ValueError('Usar batch_size >= 2 para BatchNorm.')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if device == 'auto' else torch.device(device)
    if device.type not in ('cpu', 'cuda'):
        raise ValueError('Este ejecutor contempla CPU o CUDA.')
    seed_everything(config['seed'], config['threads'])
    dataset = DragonDataset(dataset_path, config['image_size'])
    manifest, digest = dataset.manifest()
    if config.get('dataset_manifest_sha256') not in (None, digest):
        raise ValueError('El dataset no coincide con la huella declarada.')
    config['dataset_manifest_sha256'] = digest
    config['dataset_path'] = None  # La ruta local no forma parte de la identidad portable.
    output = Path(output)
    if output.exists() and any(output.iterdir()) and not resume:
        raise FileExistsError('La carpeta contiene resultados. Usar otra ruta o --resume.')
    loader_rng = torch.Generator().manual_seed(config['seed'])
    input_noise_rng = torch.Generator(device=device).manual_seed(config['seed'] + 2)
    augment_rng = torch.Generator().manual_seed(config['seed'] + 3)
    loader = DataLoader(dataset, batch_size=config['batch_size'], shuffle=True,
                        num_workers=0, generator=loader_rng, drop_last=False)
    generator, discriminator = build_models(config, device)
    if config.get('isolate_init_rng', False):
        # La normalización espectral consume aleatoriedad al construir D; reiniciar aquí
        # mantiene idéntica la secuencia de z de entrenamiento entre variantes.
        torch.manual_seed(config['seed'] + 4)
    optimizer_g = torch.optim.Adam(generator.parameters(), lr=config['learning_rate_g'], betas=(0.5, 0.999))
    optimizer_d = torch.optim.Adam(discriminator.parameters(), lr=config['learning_rate_d'], betas=(0.5, 0.999))
    fixed_noise = torch.randn(config['fixed_noise_count'], config['latent_dim'], 1, 1,
                              generator=torch.Generator().manual_seed(config['seed'] + 1)).to(device)
    history = []
    start = 0
    hypothesis = hypothesis or HYPOTHESES[experiment]
    environment = {'python': platform.python_version(), 'torch': str(torch.__version__),
                   'numpy': np.__version__, 'device': str(device), 'threads': config['threads'],
                   'gpu': torch.cuda.get_device_name(device) if device.type == 'cuda' else None}
    if resume:
        saved = torch.load(resume, map_location='cpu', weights_only=True)
        if saved['config'] != config or saved['experiment'] != experiment:
            raise ValueError('La configuración o el dataset difiere del checkpoint.')
        if saved['environment'] != environment:
            raise ValueError('Reanudar en el mismo entorno y dispositivo para conservar los controles.')
        if hypothesis != saved['hypothesis']:
            raise ValueError('La hipótesis debe coincidir con la registrada antes de entrenar.')
        if config['discriminator_input_noise_std'] and 'input_noise' not in saved['rng']:
            raise ValueError('Checkpoint de estabilización anterior al control de ruido; reiniciar esa ejecución.')
        generator.load_state_dict(saved['generator'])
        discriminator.load_state_dict(saved['discriminator'])
        optimizer_g.load_state_dict(saved['optimizer_g'])
        optimizer_d.load_state_dict(saved['optimizer_d'])
        fixed_noise = saved['fixed_noise'].to(device)
        history, start = saved['history'], saved['epoch']
        restore_rng(saved['rng'], loader_rng, input_noise_rng, augment_rng)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'samples').mkdir(exist_ok=True)
    if snapshot_every:
        (output / 'snapshots').mkdir(exist_ok=True)
    write_json(output / 'config.json', config)
    write_json(output / 'dataset_manifest.json', manifest)
    write_json(output / 'environment.json', environment)
    (output / 'hypothesis.txt').write_text(hypothesis + '\n', encoding='utf-8')
    torch.save(fixed_noise.cpu(), output / 'fixed_noise.pt')
    if start == 0:
        save_grid(generator, fixed_noise, output / 'samples' / 'epoch_0000.png')
    end = config['epochs'] if stop_after is None else min(config['epochs'], stop_after)
    if end < start:
        raise ValueError('El punto de parada es anterior al checkpoint.')
    for epoch in range(start + 1, end + 1):
        started = time.perf_counter()
        totals = np.zeros(4, dtype=np.float64)
        seen = 0
        for real in loader:
            if config.get('augment_hflip', False):
                real = horizontal_flip(real, augment_rng)
            real = real.to(device)
            batch = len(real)
            optimizer_d.zero_grad(set_to_none=True)
            noise = torch.randn(batch, config['latent_dim'], 1, 1, device=device)
            fake = generator(noise)
            std = config['discriminator_input_noise_std']
            real_logits = discriminator(add_noise(real, std, input_noise_rng))
            fake_logits = discriminator(add_noise(fake.detach(), std, input_noise_rng))
            loss_d = (F.softplus(-real_logits).mean() + F.softplus(fake_logits).mean()) / 2
            loss_d.backward()
            optimizer_d.step()
            optimizer_g.zero_grad(set_to_none=True)
            discriminator.requires_grad_(False)
            logits = discriminator(add_noise(fake, std, input_noise_rng))
            loss_g = generator_loss(logits, config['generator_loss'])
            loss_g.backward()
            optimizer_g.step()
            discriminator.requires_grad_(True)
            values = [loss_g.item(), loss_d.item(), real_logits.detach().sigmoid().mean().item(),
                      fake_logits.detach().sigmoid().mean().item()]
            if not np.isfinite(values).all():
                raise FloatingPointError('Pérdidas no finitas. Revisar configuración y último checkpoint.')
            totals += np.asarray(values) * batch
            seen += batch
        averages = totals / seen
        history.append(dict(zip(['loss_g', 'loss_d', 'd_real', 'd_fake'], averages.tolist()),
                            epoch=epoch, seconds=time.perf_counter() - started, images_seen=seen))
        save_grid(generator, fixed_noise, output / 'samples' / f'epoch_{epoch:04d}.png')
        if snapshot_every and epoch % snapshot_every == 0:
            # Solo G: suficiente para generar candidatos de épocas intermedias con generate.py.
            torch.save({'config': config, 'experiment': experiment, 'epoch': epoch,
                        'generator': generator.state_dict()},
                       output / 'snapshots' / f'generator_epoch_{epoch:04d}.pt')
        if epoch % checkpoint_every == 0 or epoch == end:
            checkpoint = {'config': config, 'experiment': experiment, 'epoch': epoch,
                          'environment': environment, 'hypothesis': hypothesis, 'history': history,
                          'generator': generator.state_dict(), 'discriminator': discriminator.state_dict(),
                          'optimizer_g': optimizer_g.state_dict(), 'optimizer_d': optimizer_d.state_dict(),
                          'fixed_noise': fixed_noise.cpu(),
                          'rng': rng_state(loader_rng, input_noise_rng, augment_rng)}
            atomic_save(checkpoint, output / 'last.pt')
        save_history(history, output)
        print(f'Época {epoch}/{config["epochs"]}: G={averages[0]:.4f}, D={averages[1]:.4f}, '
              f'{history[-1]["seconds"]:.1f}s', flush=True)
    if history:
        save_history(history, output)
    return output / 'last.pt'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default='configs/base.json')
    parser.add_argument('--data', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--experiment', choices=list(HYPOTHESES), default='base')
    parser.add_argument('--device', choices=['auto', 'cpu', 'cuda'], default='auto')
    parser.add_argument('--resume')
    parser.add_argument('--hypothesis-file', help='Hipótesis propia escrita antes de entrenar.')
    parser.add_argument('--stop-after', type=int, help='Parar después de esta época para una prueba o interrupción planificada.')
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding='utf-8'))
    hypothesis = Path(args.hypothesis_file).read_text(encoding='utf-8').strip() if args.hypothesis_file else None
    train(config, args.data, args.output, args.experiment, args.device, args.resume,
          hypothesis, args.stop_after)


if __name__ == '__main__':
    main()
