"""Arma la galería final a partir de la selección y del manifiesto de candidatos."""

import argparse
import csv
import json
import shutil
from pathlib import Path

from PIL import Image

CRITERIA = 'docs/criterios_evaluacion.md'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidates', type=Path, required=True, help='Carpeta con PNG y manifest.json.')
    parser.add_argument('--selection', type=Path, default=Path('docs/data/seleccion_final.csv'),
                        help='CSV con columnas file y motivo; opcionales nombre y clase.')
    parser.add_argument('--output', type=Path, default=Path('galeria'))
    parser.add_argument('--mosaic', type=Path, default=Path('docs/img/galeria_mosaico.png'))
    parser.add_argument('--total', type=int, help='Candidatos generados en total, si hubo varias tandas.')
    args = parser.parse_args()

    manifest = json.loads((args.candidates / 'manifest.json').read_text(encoding='utf-8'))
    candidates = {row['file']: row for row in manifest['characters']}
    with args.selection.open(encoding='utf-8-sig', newline='') as source:
        selection = list(csv.DictReader(source))
    if len({row['file'] for row in selection}) != len(selection):
        raise ValueError('La selección repite archivos.')
    if args.output.exists() and any(args.output.iterdir()):
        raise FileExistsError('La carpeta de la galería debe estar vacía.')
    args.output.mkdir(parents=True, exist_ok=True)

    total = args.total or manifest['source_generated_count']
    rate = len(selection) / total * 100
    characters, record = [], []
    for number, row in enumerate(selection, start=1):
        source = candidates[row['file']]
        name = f'personaje_{number:02d}.png'
        shutil.copyfile(args.candidates / row['file'], args.output / name)
        # Mismo formato que lee dragon_gan.generate --manifest para regenerar.
        characters.append({'file': name, 'seed': source['seed'], 'z': source['z']})
        # nombre y clase son opcionales (bonificación del enunciado).
        record.append({'id': name, 'candidato': row['file'], 'seed': source['seed'],
                       'nombre': row.get('nombre', ''), 'clase': row.get('clase', ''), 'motivo': row['motivo']})

    regeneration = {'checkpoint_sha256': manifest['checkpoint_sha256'], 'source_generated_count': total,
                    'characters': characters, 'selection_criteria': CRITERIA, 'status': 'final_gallery'}
    (args.output / 'galeria_selection.json').write_text(json.dumps(regeneration, indent=2), encoding='utf-8')
    with (args.output / 'registro_seleccion.csv').open('w', encoding='utf-8', newline='') as target:
        writer = csv.DictWriter(target, fieldnames=record[0].keys())
        writer.writeheader()
        writer.writerows(record)

    # Mosaico ampliado para la presentación; los PNG individuales no se modifican.
    mosaic = Image.new('RGB', (5 * 200, -(-len(characters) // 5) * 200), 'white')
    for index, row in enumerate(characters):
        with Image.open(args.output / row['file']) as picture:
            mosaic.paste(picture.convert('RGB').resize((192, 192), Image.Resampling.BICUBIC),
                         (index % 5 * 200 + 4, index // 5 * 200 + 4))
    mosaic.save(args.mosaic)

    print(f'Personajes: {len(selection)}. Candidatos generados: {total}.')
    print(f'Tasa de selección: {len(selection)} / {total} × 100 = {rate:.1f} %')
    if len(selection) < 10:
        print('AVISO: el enunciado exige al menos 10 personajes.')


if __name__ == '__main__':
    main()
