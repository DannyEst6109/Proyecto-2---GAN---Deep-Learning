"""Hojas de contacto para revisar candidatos sin modificar sus PNG originales."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def contact_sheets(folder, output):
    folder, output = Path(folder), Path(output)
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    if output.exists() and any(output.iterdir()):
        raise FileExistsError('La carpeta de hojas debe estar vacía.')
    output.mkdir(parents=True, exist_ok=True)
    rows = manifest['characters']
    for page, start in enumerate(range(0, len(rows), 50)):
        canvas = Image.new('RGB', (800, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        for index, row in enumerate(rows[start:start + 50]):
            name = row['file']
            if Path(name).name != name:
                raise ValueError('Cada imagen debe ser un nombre sin subcarpetas.')
            x, y = (index % 10) * 80, (index // 10) * 100
            with Image.open(folder / name) as picture:
                canvas.paste(ImageOps.contain(picture.convert('RGB'), (80, 80)), (x, y))
            draw.text((x + 2, y + 82), name.removesuffix('.png').removeprefix('dragon_'), fill='black')
        canvas.save(output / f'page_{page + 1:02d}.png')
    print(f'{len(rows)} candidatos en {(len(rows) + 49) // 50} hojas: {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidates', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    contact_sheets(args.candidates, args.output)


if __name__ == '__main__':
    main()
