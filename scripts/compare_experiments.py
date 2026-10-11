"""Verifica controles y produce figuras y una ficha para interpretación humana."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageOps
import torch

from dragon_gan.train import variant_config, write_json
from scripts.run_experiments import EXPERIMENTS


def compare(root, output):
    root, output = Path(root), Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('Usar una carpeta vacía para no sobrescribir la interpretación anterior.')
    plan = json.loads((root / 'plan.json').read_text(encoding='utf-8'))
    runs = {}
    for name in EXPERIMENTS:
        folder = root / name
        config = json.loads((folder / 'config.json').read_text(encoding='utf-8'))
        manifest = json.loads((folder / 'dataset_manifest.json').read_text(encoding='utf-8'))
        encoded = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        if hashlib.sha256(encoded).hexdigest() != config['dataset_manifest_sha256']:
            raise ValueError(f'{name}: manifiesto y hash distintos.')
        expected = variant_config(dict(plan['config'], dataset_path=None), name)
        if config != expected:
            raise ValueError(f'{name}: configuración distinta del plan de un solo factor.')
        if (folder / 'hypothesis.txt').read_text(encoding='utf-8').strip() != plan['hypotheses'][name]:
            raise ValueError(f'{name}: hipótesis distinta del plan previo.')
        with (folder / 'losses.csv').open(encoding='utf-8', newline='') as source:
            history = [{key: float(value) for key, value in row.items()} for row in csv.DictReader(source)]
        if not history or any(not math.isfinite(value) for row in history for value in row.values()):
            raise ValueError(f'{name}: registros vacíos o no finitos.')
        if [row['epoch'] for row in history] != list(range(1, len(history) + 1)):
            raise ValueError(f'{name}: historial de épocas incompleto.')
        if any(row['images_seen'] != len(manifest) for row in history):
            raise ValueError(f'{name}: no se registraron todas las imágenes por época.')
        runs[name] = {'config': config, 'history': history, 'manifest': manifest,
                      'environment': json.loads((folder / 'environment.json').read_text(encoding='utf-8')),
                      'fixed_noise': torch.load(folder / 'fixed_noise.pt', map_location='cpu', weights_only=True),
                      'initial': (folder / 'samples/epoch_0000.png').read_bytes()}
    base = runs['base']
    for name, run in runs.items():
        if run['manifest'] != base['manifest'] or run['environment'] != base['environment']:
            raise ValueError(f'{name}: datos o entorno diferentes.')
        if not torch.equal(run['fixed_noise'], base['fixed_noise']) or run['initial'] != base['initial']:
            raise ValueError(f'{name}: ruido fijo o muestras iniciales diferentes.')
        if len(run['history']) != len(base['history']):
            raise ValueError('Comparar solo ejecuciones con el mismo número de épocas completas.')
    output.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(2, 2, figsize=(12, 8))
    for name, run in runs.items():
        x = [row['epoch'] for row in run['history']]
        for axis, key, title in zip(axes.flat, ('loss_d', 'loss_g', 'd_real', 'd_fake'),
                                   ('Pérdida D', 'Pérdida G: objetivos distintos', 'D(real)', 'D(fake)')):
            axis.plot(x, [row[key] for row in run['history']], marker='.', label=name)
            axis.set(xlabel='Época', title=title)
            axis.legend()
    figure.suptitle(f'{plan["purpose"]}: curvas descriptivas; requieren evaluación visual')
    figure.tight_layout()
    figure.savefig(output / 'comparison.png', dpi=150)
    plt.close(figure)
    last_epoch = len(base['history'])
    epochs = sorted({0, *(max(1, last_epoch * k // 4) for k in (1, 2, 3)), last_epoch})
    tile = 320
    canvas = Image.new('RGB', (tile * len(EXPERIMENTS), (tile + 30) * len(epochs)), 'white')
    draw = ImageDraw.Draw(canvas)
    for row, epoch in enumerate(epochs):
        for column, name in enumerate(EXPERIMENTS):
            x, y = column * tile, row * (tile + 30)
            draw.text((x + 5, y + 5), f'{name} | epoch {epoch}', fill='black')
            with Image.open(root / name / 'samples' / f'epoch_{epoch:04d}.png') as picture:
                canvas.paste(ImageOps.contain(picture.convert('RGB'), (tile, tile)), (x, y + 30))
    canvas.save(output / 'fixed_noise_comparison.png')
    report = {'purpose': plan['purpose'], 'training_images': len(base['manifest']),
              'controls_verified': ['single_factor_configs', 'same_dataset', 'same_environment',
                                    'same_fixed_noise', 'same_initial_samples', 'same_completed_epochs'],
              'epochs_completed': last_epoch, 'epochs_planned': base['config']['epochs'],
              'all_epochs_completed': last_epoch == base['config']['epochs'],
              'runs': {name: {'final': run['history'][-1],
                              'training_loop_seconds': sum(row['seconds'] for row in run['history'])}
                       for name, run in runs.items()},
              'interpretation': 'PENDING_MANUAL_REVIEW', 'selected_model': None,
              'limitations': ['Las pérdidas de G tienen objetivos diferentes.',
                              'D(real) y D(fake) son puntuaciones de entrenamiento, no métricas de calidad.',
                              'Una semilla no demuestra robustez estadística.',
                              'El piloto no demuestra diversidad, novedad ni aptitud para la entrega final.']}
    write_json(output / 'summary.json', report)
    (output / 'interpretation.md').write_text(
        '# Interpretación pendiente\n\n'
        f'Tipo: {plan["purpose"]}. Imágenes: {len(base["manifest"])}. Épocas: {last_epoch}.\n\n'
        'Completar mediante revisión de las figuras, sin inferir calidad solo de las pérdidas.\n\n'
        '- Reconocimiento y coherencia de las mismas posiciones de ruido fijo:\n'
        '- Diversidad y posible repetición entre posiciones:\n'
        '- Relación entre pérdidas, puntuaciones de D y cambios visuales:\n'
        '- Hipótesis de pérdida: evidencia a favor/en contra o resultado inconcluso:\n'
        '- Hipótesis de estabilización: evidencia a favor/en contra o resultado inconcluso:\n'
        '- Modelo propuesto y razón; dejar sin elegir si faltan resultados útiles:\n'
        '- Limitaciones y evidencias que faltan:\n', encoding='utf-8')
    print(f'Controles verificados. Figuras y ficha: {output}')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    compare(args.runs, args.output)


if __name__ == '__main__':
    main()
