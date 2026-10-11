"""Generar candidatos o regenerar PNG a partir de sus vectores z guardados."""

import argparse
import hashlib
import json
from pathlib import Path

import torch
from torchvision.utils import save_image

from .models import Generator
from .train import write_json


def generate(checkpoint, output, count=200, seed=1000, manifest=None):
    if count < 1:
        raise ValueError('La cantidad debe ser positiva.')
    saved = torch.load(checkpoint, map_location='cpu', weights_only=True)
    config = saved['config']
    torch.set_num_threads(config['threads'])
    generator = Generator(config['latent_dim'], config['channels'], config['features'])
    generator.load_state_dict(saved['generator'])
    generator.eval()
    if manifest:
        source = json.loads(Path(manifest).read_text(encoding='utf-8'))
        vectors = source['characters']
        if hashlib.sha256(Path(checkpoint).read_bytes()).hexdigest() != source['checkpoint_sha256']:
            raise ValueError('La regeneración requiere exactamente el checkpoint declarado.')
    else:
        vectors = []
        for index in range(count):
            sample_seed = seed + index
            z = torch.randn(config['latent_dim'], generator=torch.Generator().manual_seed(sample_seed))
            vectors.append({'file': f'dragon_{index + 1:04d}.png', 'seed': sample_seed, 'z': z.tolist()})
    output = Path(output)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('La carpeta de salida debe estar vacía para preservar la selección anterior.')
    output.mkdir(parents=True, exist_ok=True)
    with torch.no_grad():
        for row in vectors:
            name = row['file']
            if Path(name).name != name or not name.endswith('.png'):
                raise ValueError('Cada archivo debe ser un nombre PNG sin subcarpetas.')
            z = torch.tensor(row['z'], dtype=torch.float32).reshape(1, config['latent_dim'], 1, 1)
            save_image(generator(z), output / name, normalize=True, value_range=(-1, 1))
    result = {'checkpoint_sha256': hashlib.sha256(Path(checkpoint).read_bytes()).hexdigest(),
              'source_generated_count': source['source_generated_count'] if manifest else count,
              'characters': vectors, 'selection_criteria': source.get('selection_criteria') if manifest else None,
              'status': source.get('status', 'candidates') if manifest else 'candidates'}
    write_json(output / 'manifest.json', result)
    print(f'{len(vectors)} PNG guardados en {output}. No constituyen prueba de novedad.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--count', type=int, default=200)
    parser.add_argument('--seed', type=int, default=1000)
    parser.add_argument('--manifest', help='Manifiesto seleccionado para regenerar sus personajes.')
    args = parser.parse_args()
    generate(args.checkpoint, args.output, args.count, args.seed, args.manifest)


if __name__ == '__main__':
    main()
