"""Cierra la selección de persona 2: todos los dragones del ZIP menos las exclusiones revisadas."""

import argparse
import csv
from collections import Counter
from pathlib import Path

ACCEPTED = 'Dragón reconocible; sin texto, marco de carta ni recorte extremo.'


def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as source:
        return list(csv.DictReader(source))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('docs/data/curation_final_v4.csv'),
                        help='Listado con los 965 dragones del ZIP.')
    parser.add_argument('--exclusions', type=Path, default=Path('docs/data/exclusiones_persona2.csv'))
    parser.add_argument('--output', type=Path, default=Path('docs/data/curation_final_v4.csv'))
    args = parser.parse_args()

    excluded = {row['file']: row['reason'] for row in read_csv(args.exclusions)}
    rows = read_csv(args.source)
    names = {Path(row['source_path']).name for row in rows}
    missing = set(excluded) - names
    if missing:
        raise ValueError(f'Exclusiones que no existen en el dataset: {missing}')

    counts = Counter()
    for row in rows:
        reason = excluded.get(Path(row['source_path']).name)
        row['decision'] = 'descartar' if reason else 'aceptar_entrenamiento'
        row['reason'] = reason or ACCEPTED
        counts[row['source_path'].split('/')[0], row['decision']] += 1

    with args.output.open('w', encoding='utf-8', newline='') as target:
        writer = csv.DictWriter(target, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for (split, decision), count in sorted(counts.items()):
        print(f'{split:5} {decision:22} {count}')


if __name__ == '__main__':
    main()
