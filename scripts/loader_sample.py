"""Comprueba el dataset tal como lo ve la GAN y guarda una muestra visual.

Ejecutar desde la raíz: python -m scripts.loader_sample
"""

import argparse
from pathlib import Path

import torch
from torchvision.utils import save_image

from dragon_gan.data import DragonDataset


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', default='data/dragons_final_v4')
    parser.add_argument('--output', type=Path, default=Path('docs/img/muestra_cargador.png'))
    parser.add_argument('--count', type=int, default=64)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    dataset = DragonDataset(args.data)
    images = torch.stack([dataset[i] for i in range(len(dataset))])
    assert images.shape[1:] == (3, 64, 64), images.shape
    assert images.min() >= -1 and images.max() <= 1

    chosen = torch.randperm(len(dataset), generator=torch.Generator().manual_seed(args.seed))[:args.count]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_image(images[chosen], args.output, nrow=8, normalize=True, value_range=(-1, 1))

    print(f'Imágenes cargadas: {len(dataset)}')
    print(f'Forma: {tuple(images.shape)}, rango: [{images.min():.2f}, {images.max():.2f}]')
    print(f'Media por canal: {[round(v, 3) for v in images.mean(dim=(0, 2, 3)).tolist()]}')
    print(f'Huella del manifiesto: {dataset.manifest()[1]}')
    print(f'Muestra guardada: {args.output}')


if __name__ == '__main__':
    main()
