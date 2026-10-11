"""Vecinos más cercanos de cada personaje generado dentro del dataset de entrenamiento.

Ejecutar desde la raíz: python -m scripts.nearest_neighbors --generated galeria
"""

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision.models import ResNet18_Weights, resnet18
from torchvision.transforms.functional import to_tensor

from dragon_gan.data import DragonDataset


def cnn_features(images):
    """Características de ResNet-18 preentrenada en ImageNet (512 valores por imagen)."""
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    model.fc = torch.nn.Identity()
    model.eval()
    mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
    outputs = []
    with torch.no_grad():
        for batch in images.split(64):
            batch = F.interpolate(batch / 2 + 0.5, size=224, mode='bilinear', align_corners=False)
            outputs.append(model((batch - mean) / std))
    outputs = torch.cat(outputs)
    # Norma fija: la distancia depende solo del ángulo entre vectores.
    return F.normalize(outputs, dim=1) * outputs.shape[1] ** 0.5


def features(images, metric):
    """pixel: los 64×64×3 valores. forma: grises 16×16 sin brillo ni contraste. cnn: ResNet-18."""
    if metric == 'pixel':
        return images.flatten(1)
    if metric == 'cnn':
        return cnn_features(images)
    small = F.avg_pool2d(images.mean(dim=1, keepdim=True), 4).flatten(1)
    small = small - small.mean(dim=1, keepdim=True)
    return small / small.std(dim=1, keepdim=True).clamp_min(1e-6)


def distances(a, b):
    """Raíz del error cuadrático medio entre cada par de filas."""
    return torch.cdist(a, b) / a.shape[1] ** 0.5


def load_generated(folder, size=64):
    files = sorted(Path(folder).glob('*.png'))
    if not files:
        raise FileNotFoundError(f'No hay PNG en {folder}')
    images = [to_tensor(Image.open(p).convert('RGB').resize((size, size))) * 2 - 1 for p in files]
    return files, torch.stack(images)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generated', required=True, help='Carpeta con los PNG generados.')
    parser.add_argument('--data', default='data/dragons_final_v4')
    parser.add_argument('--output', type=Path, default=Path('docs/vecinos'))
    parser.add_argument('--metric', choices=['cnn', 'pixel', 'forma'], default='cnn')
    parser.add_argument('--k', type=int, default=5)
    args = parser.parse_args()

    dataset = DragonDataset(args.data)
    train = torch.stack([dataset[i] for i in range(len(dataset))])
    # El entrenamiento usa volteo horizontal: también se compara con las imágenes volteadas.
    train_all = torch.cat([train, train.flip(3)])
    train_features = features(train_all, args.metric)
    files, generated = load_generated(args.generated)
    nearest = distances(features(generated, args.metric), train_features).topk(args.k, largest=False)

    # Referencia: distancia de cada imagen real a su vecina real más cercana (sin contarse a sí misma).
    real = distances(features(train, args.metric), train_features)
    own = torch.arange(len(train))
    real[own, own] = float('inf')
    reference = real.min(dim=1).values
    p5, median = reference.quantile(0.05).item(), reference.median().item()

    args.output.mkdir(parents=True, exist_ok=True)
    rows = []
    figure, axes = plt.subplots(len(files), args.k + 1, squeeze=False,
                                figsize=(1.6 * (args.k + 1), 1.8 * len(files)))
    for i, path in enumerate(files):
        axes[i, 0].imshow(generated[i].permute(1, 2, 0) / 2 + 0.5)
        axes[i, 0].set_title(path.stem, fontsize=7)
        for rank in range(args.k):
            index, distance = nearest.indices[i, rank].item(), nearest.values[i, rank].item()
            flipped = index >= len(train)
            neighbor = dataset.files[index % len(train)].name
            axes[i, rank + 1].imshow(train_all[index].permute(1, 2, 0) / 2 + 0.5)
            axes[i, rank + 1].set_title(f'{distance:.3f}' + (' (volteada)' if flipped else ''), fontsize=7)
            rows.append({'generated': path.name, 'rank': rank + 1, 'neighbor': neighbor,
                         'flipped': 'si' if flipped else 'no', 'distance': round(distance, 4),
                         'below_real_p5': 'si' if distance < p5 else 'no'})
    for axis in axes.flat:
        axis.axis('off')
    figure.suptitle(f'Generada y sus {args.k} vecinas ({args.metric}); referencia real p5={p5:.3f}', fontsize=8)
    figure.tight_layout()
    figure.savefig(args.output / f'vecinos_{args.metric}.png', dpi=150)

    with (args.output / f'vecinos_{args.metric}.csv').open('w', encoding='utf-8', newline='') as target:
        writer = csv.DictWriter(target, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f'Métrica: {args.metric}. Entrenamiento: {len(train)} imágenes (más volteadas).')
    print(f'Referencia entre reales: p5={p5:.3f}, mediana={median:.3f}')
    for i, path in enumerate(files):
        closest = nearest.values[i, 0].item()
        note = 'REVISAR: más cerca que el 5 % de las reales' if closest < p5 else 'sin alerta'
        print(f'{path.name}: vecino más cercano a {closest:.3f} ({note})')


if __name__ == '__main__':
    main()
