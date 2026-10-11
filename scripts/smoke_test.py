"""Prueba técnica con imágenes sintéticas temporales; no es evidencia del proyecto.

Ejecutar desde la raíz: python -m scripts.smoke_test
"""

import json
import tempfile
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from dragon_gan.generate import generate
from dragon_gan.data import DragonDataset
from dragon_gan.train import generator_loss, train
from scripts.compare_experiments import compare
from scripts.run_experiments import run_suite


def main():
    config = json.loads(Path('configs/base.json').read_text(encoding='utf-8'))
    config.update(features=8, latent_dim=8, batch_size=2, epochs=2,
                  fixed_noise_count=4, threads=1)
    with tempfile.TemporaryDirectory(prefix='dragon_gan_smoke_') as temporary:
        root = Path(temporary)
        data = root / 'data'
        data.mkdir()
        rng = np.random.default_rng(123)
        for index in range(5):
            image = rng.integers(0, 256, size=(48, 80, 3), dtype=np.uint8)
            Image.fromarray(image).save(data / f'{index}.png')
        full = train(config, data, root / 'full', device='cpu')
        partial = train(config, data, root / 'resume', device='cpu', stop_after=1)
        resumed = train(config, data, root / 'resume', device='cpu', resume=partial)
        a = torch.load(full, weights_only=True)
        b = torch.load(resumed, weights_only=True)
        for model in ('generator', 'discriminator'):
            for key in a[model]:
                assert torch.equal(a[model][key], b[model][key]), f'Reanudación distinta: {model}.{key}'
        for row_a, row_b in zip(a['history'], b['history']):
            for key in ('epoch', 'loss_g', 'loss_d', 'd_real', 'd_fake', 'images_seen'):
                assert row_a[key] == row_b[key], f'Registro distinto: {key}'
        for experiment, changed_key in [('loss', 'generator_loss'),
                                        ('stabilization', 'discriminator_input_noise_std')]:
            path = train(config, data, root / experiment, experiment=experiment, device='cpu')
            variant = torch.load(path, weights_only=True)
            differences = {key for key in a['config'] if a['config'][key] != variant['config'][key]}
            assert differences == {changed_key}, differences
            assert torch.equal(a['fixed_noise'], variant['fixed_noise'])
            assert torch.equal(a['rng']['torch'], variant['rng']['torch']), 'Vectores de entrenamiento desalineados'
            assert torch.equal(a['rng']['loader'], variant['rng']['loader']), 'Orden de datos desalineado'
            assert (root / 'full/samples/epoch_0000.png').read_bytes() == (root / experiment / 'samples/epoch_0000.png').read_bytes()
            if experiment == 'stabilization':
                path_partial = train(config, data, root / 'noise_resume', experiment=experiment,
                                     device='cpu', stop_after=1)
                path_resumed = train(config, data, root / 'noise_resume', experiment=experiment,
                                     device='cpu', resume=path_partial)
                noise_resumed = torch.load(path_resumed, weights_only=True)
                for model in ('generator', 'discriminator'):
                    assert all(torch.equal(variant[model][key], noise_resumed[model][key])
                               for key in variant[model]), 'Reanudación de ruido distinta'
        # v3: normalización espectral como cambio único, volteo horizontal y snapshots.
        v3 = dict(config, discriminator_spectral_norm=False, augment_hflip=True, isolate_init_rng=True, snapshot_every=1, checkpoint_every=2,
                  stabilization_change={'discriminator_spectral_norm': True})
        v3_base = torch.load(train(v3, data, root / 'v3_base', device='cpu'), weights_only=True)
        v3_sn = torch.load(train(v3, data, root / 'v3_sn', experiment='stabilization', device='cpu'),
                           weights_only=True)
        differences = {key for key in v3_base['config'] if v3_base['config'][key] != v3_sn['config'][key]}
        assert differences == {'discriminator_spectral_norm'}, differences
        assert torch.equal(v3_base['rng']['torch'], v3_sn['rng']['torch']), 'SN desalineó los vectores z'
        assert torch.equal(v3_base['rng']['augment'], v3_sn['rng']['augment'])
        assert any('parametrizations' in key for key in v3_sn['discriminator'])
        assert (root / 'v3_base/samples/epoch_0000.png').read_bytes() == (root / 'v3_sn/samples/epoch_0000.png').read_bytes(), 'SN cambió la inicialización de G'
        snapshot = root / 'v3_sn/snapshots/generator_epoch_0001.pt'
        generate(snapshot, root / 'snapshot_candidates', count=2)
        v3_partial = train(v3, data, root / 'v3_resume', experiment='stabilization', device='cpu', stop_after=1)
        v3_resumed = torch.load(train(v3, data, root / 'v3_resume', experiment='stabilization', device='cpu',
                                      resume=v3_partial), weights_only=True)
        for key in v3_sn['generator']:
            assert torch.equal(v3_sn['generator'][key], v3_resumed['generator'][key]), 'Reanudación v3 distinta'
        for kind in ('non_saturating', 'minimax'):
            logits = torch.tensor([-100.0, 0.0, 100.0], requires_grad=True)
            loss = generator_loss(logits, kind)
            loss.backward()
            assert torch.isfinite(loss) and torch.isfinite(logits.grad).all()
            expected = -torch.sigmoid(-logits.detach()) / 3 if kind == 'non_saturating' else -torch.sigmoid(logits.detach()) / 3
            assert torch.allclose(logits.grad, expected)
        generate(full, root / 'candidates', count=3)
        generate(full, root / 'regenerated', manifest=root / 'candidates/manifest.json')
        for image in (root / 'candidates').glob('*.png'):
            assert image.read_bytes() == (root / 'regenerated' / image.name).read_bytes()
        suite_config = dict(config, dataset_manifest_sha256=DragonDataset(data).manifest()[1])
        suite_config_path = root / 'suite_config.json'
        suite_config_path.write_text(json.dumps(suite_config), encoding='utf-8')
        run_suite(suite_config_path, data, root / 'suite')
        report = compare(root / 'suite', root / 'comparison')
        assert report['all_epochs_completed'] and report['purpose'] == 'pilot'
        assert report['selected_model'] is None
        altered_path = root / 'suite/loss/config.json'
        altered = json.loads(altered_path.read_text())
        altered['seed'] += 1
        altered_path.write_text(json.dumps(altered), encoding='utf-8')
        try:
            compare(root / 'suite', root / 'invalid_comparison')
        except ValueError as error:
            assert 'un solo factor' in str(error)
        else:
            raise AssertionError('Se aceptó comparar experimentos con distinta semilla.')
        # Impedir reanudar con imágenes diferentes bajo las mismas rutas.
        Image.new('RGB', (80, 48), 'black').save(data / '0.png')
        try:
            train(config, data, root / 'resume', device='cpu', resume=resumed)
        except ValueError as error:
            assert 'configuración o el dataset' in str(error)
        else:
            raise AssertionError('Se permitió reanudar con un dataset cambiado.')
    print('OK: tres variantes, controles, pérdidas finitas, reanudación exacta y regeneración idéntica.')
    print('Los datos y resultados sintéticos temporales se eliminaron. No son dragones ni galería final.')


if __name__ == '__main__':
    main()
