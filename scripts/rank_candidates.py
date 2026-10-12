"""Prefiltro de candidatos: los ordena por cercanía a dragones reales según ResNet-18.

Ejecutar desde la raíz: python -m scripts.rank_candidates --candidates runs/candidates_2000
"""

import argparse
import csv
from pathlib import Path

import torch
from PIL import Image, ImageDraw

from dragon_gan.data import DragonDataset
from scripts.nearest_neighbors import distances, features, load_generated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidates', required=True)
    parser.add_argument('--data', default='data/dragons_final_v4')
    parser.add_argument('--output', type=Path, default=Path('docs/data/prefiltro_candidatos.csv'))
    parser.add_argument('--sheets', type=Path, help='Carpeta para hojas de contacto de los primeros.')
    parser.add_argument('--top', type=int, default=400)
    args = parser.parse_args()

    dataset = DragonDataset(args.data)
    train = torch.stack([dataset[i] for i in range(len(dataset))])
    files, generated = load_generated(args.candidates)
    train_features = features(torch.cat([train, train.flip(3)]), 'cnn')
    nearest = distances(features(generated, 'cnn'), train_features).min(dim=1).values
    order = nearest.argsort().tolist()

    with args.output.open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['rank', 'file', 'cnn_distance', 'revisado'])
        for rank, index in enumerate(order, start=1):
            writer.writerow([rank, files[index].name, round(nearest[index].item(), 4),
                             'si' if rank <= args.top else 'no'])

    if args.sheets:
        args.sheets.mkdir(parents=True, exist_ok=True)
        for start in range(0, args.top, 100):
            canvas = Image.new('RGB', (10 * 128, 10 * 140), 'white')
            draw = ImageDraw.Draw(canvas)
            for k, index in enumerate(order[start:start + 100]):
                x, y = (k % 10) * 128, (k // 10) * 140
                with Image.open(files[index]) as picture:
                    canvas.paste(picture.convert('RGB').resize((128, 128), Image.Resampling.BICUBIC), (x, y))
                draw.text((x + 2, y + 128), files[index].stem[-4:], fill='black')
            canvas.save(args.sheets / f'top_{start // 100 + 1}.png')
    print(f'{len(files)} candidatos ordenados; se revisan los primeros {args.top}.')


if __name__ == '__main__':
    main()
