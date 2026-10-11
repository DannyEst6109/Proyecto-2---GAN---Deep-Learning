"""Ejecuta las tres variantes con una configuración y datos congelados."""

import argparse
import hashlib
import json
from pathlib import Path

from dragon_gan.data import DragonDataset
from dragon_gan.train import train, write_json

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ('base', 'loss', 'stabilization')


def run_suite(config_path, data, output, device='cpu', purpose='pilot', resume=False, dry_run=False,
              hypotheses_dir='docs/hypotheses', only=EXPERIMENTS):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    dataset = DragonDataset(data, config['image_size'])
    _, digest = dataset.manifest()
    if config.get('dataset_manifest_sha256') != digest:
        raise ValueError('Fijar el hash del dataset en la configuración antes de comparar.')
    pilot = ROOT / 'docs/data/pilot_manifest_v1.json'
    if purpose == 'project' and pilot.exists():
        pilot_digest = json.loads(pilot.read_text(encoding='utf-8'))['dataset_manifest_sha256']
        if digest == pilot_digest:
            raise ValueError('Los seis dragones están documentados solo como piloto; usar --purpose pilot.')
    hypotheses = {name: (ROOT / hypotheses_dir / f'{name}.txt').read_text(encoding='utf-8').strip()
                  for name in EXPERIMENTS}
    sources = ('dragon_gan/train.py', 'dragon_gan/data.py', 'dragon_gan/models.py',
               'scripts/run_experiments.py')
    plan = {'purpose': purpose, 'training_images': len(dataset), 'device': device,
            'config': config, 'hypotheses': hypotheses,
            'source_sha256': {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                              for path in sources}}
    if dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    output = Path(output)
    plan_path = output / 'plan.json'
    if resume:
        if not plan_path.exists() or json.loads(plan_path.read_text(encoding='utf-8')) != plan:
            raise ValueError('Reanudar requiere el mismo plan, código, datos e hipótesis.')
    elif output.exists() and any(output.iterdir()):
        raise FileExistsError('Usar una carpeta vacía para una comparación nueva.')
    output.mkdir(parents=True, exist_ok=True)
    write_json(plan_path, plan)
    for experiment in only:
        folder = output / experiment
        checkpoint = folder / 'last.pt'
        if resume and folder.exists() and any(folder.iterdir()) and not checkpoint.exists():
            raise ValueError(f'{folder}: ejecución interrumpida sin checkpoint; conservarla y reiniciar en otra carpeta.')
        print(f'[{purpose}] {experiment}: {len(dataset)} imágenes, {config["epochs"]} épocas', flush=True)
        train(config, data, folder, experiment=experiment, device=device,
              hypothesis=hypotheses[experiment], resume=checkpoint if resume and checkpoint.exists() else None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True)
    parser.add_argument('--data', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--device', choices=['cpu', 'cuda'], default='cpu')
    parser.add_argument('--purpose', choices=['pilot', 'project'], default='pilot')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--hypotheses', default='docs/hypotheses',
                        help='Carpeta con base.txt, loss.txt y stabilization.txt escritos antes de entrenar.')
    parser.add_argument('--only', nargs='+', choices=EXPERIMENTS, default=list(EXPERIMENTS),
                        help='Variantes a ejecutar ahora; usar --resume para completar las demás después.')
    args = parser.parse_args()
    run_suite(args.config, args.data, args.output, args.device, args.purpose, args.resume, args.dry_run,
              args.hypotheses, tuple(args.only))


if __name__ == '__main__':
    main()
