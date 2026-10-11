"""Revisión técnica del dataset: archivos legibles, duplicados y hojas de contacto."""

import argparse
import csv
import hashlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}


def dhash(image):
    """Huella perceptual de 64 bits: compara cada píxel con su vecino derecho."""
    gray = np.asarray(image.convert('L').resize((9, 8), Image.Resampling.LANCZOS), dtype=np.int16)
    return (gray[:, 1:] > gray[:, :-1]).flatten()


def review(folder, max_distance=4):
    files = sorted(p for p in Path(folder).rglob('*') if p.suffix.lower() in EXTENSIONS)
    rows, hashes = [], []
    for path in files:
        row = {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
               'width': '', 'height': '', 'readable': 'no', 'uniform': '', 'exact_duplicate_of': '', 'similar_to': ''}
        try:
            with Image.open(path) as image:
                image.load()
                row.update(width=image.width, height=image.height, readable='si')
                # Sin contenido: casi todos los píxeles tienen el mismo valor.
                row['uniform'] = 'si' if np.asarray(image.convert('L')).std() < 5 else 'no'
                hashes.append(dhash(image))
        except OSError:
            hashes.append(None)
        rows.append(row)

    seen = {}
    for index, row in enumerate(rows):
        first = seen.setdefault(row['sha256'], index)
        if first != index:
            row['exact_duplicate_of'] = rows[first]['file']
    # Casi duplicados: pocas diferencias de bits entre huellas perceptuales.
    for i in range(len(rows)):
        for j in range(i):
            if hashes[i] is None or hashes[j] is None or rows[i]['exact_duplicate_of']:
                continue
            if np.count_nonzero(hashes[i] != hashes[j]) <= max_distance:
                rows[i]['similar_to'] = rows[j]['file']
                break
    return files, rows


def contact_sheets(files, output, columns=10, per_page=100, cell=96):
    output.mkdir(parents=True, exist_ok=True)
    for page, start in enumerate(range(0, len(files), per_page)):
        group = files[start:start + per_page]
        canvas = Image.new('RGB', (columns * cell, -(-len(group) // columns) * (cell + 12)), 'white')
        draw = ImageDraw.Draw(canvas)
        for index, path in enumerate(group):
            x, y = (index % columns) * cell, (index // columns) * (cell + 12)
            with Image.open(path) as image:
                canvas.paste(image.convert('RGB').resize((cell, cell)), (x, y))
            draw.text((x + 2, y + cell), str(start + index), fill='black')
        canvas.save(output / f'page_{page + 1:02d}.png')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('data/dragons_all_v3'))
    parser.add_argument('--output', type=Path, default=Path('docs/data/revision_tecnica.csv'))
    parser.add_argument('--sheets', type=Path, help='Carpeta para las hojas de contacto.')
    args = parser.parse_args()

    files, rows = review(args.data)
    with args.output.open('w', encoding='utf-8', newline='') as target:
        writer = csv.DictWriter(target, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    if args.sheets:
        contact_sheets(files, args.sheets)

    print(f'Imágenes: {len(rows)}')
    print(f"No legibles: {sum(r['readable'] == 'no' for r in rows)}")
    print(f"Sin contenido: {[r['file'] for r in rows if r['uniform'] == 'si']}")
    print(f"Duplicados exactos: {sum(bool(r['exact_duplicate_of']) for r in rows)}")
    print(f"Casi duplicados: {sum(bool(r['similar_to']) for r in rows)}")
    print(f"Tamaños: {sorted({(r['width'], r['height']) for r in rows if r['readable'] == 'si'})}")


if __name__ == '__main__':
    main()
