"""Tabla de evaluación de candidatos: crearla vacía o calcular las decisiones."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

CRITERIA = ['dragon', 'cuerpo_alas', 'universo', 'anatomia', 'distinto', 'novedad']
COLUMNS = ['file', 'seed', *CRITERIA, 'observaciones', 'decision']


def create(candidates, output):
    if output.exists():
        raise FileExistsError(f'{output} ya existe; no se sobrescribe una evaluación.')
    manifest = json.loads((candidates / 'manifest.json').read_text(encoding='utf-8'))
    with output.open('w', encoding='utf-8', newline='') as target:
        writer = csv.DictWriter(target, fieldnames=COLUMNS, restval='')
        writer.writeheader()
        for row in manifest['characters']:
            writer.writerow({'file': row['file'], 'seed': row['seed']})
    print(f"{len(manifest['characters'])} candidatos en {output}")


def decision(row):
    """Regla de docs/criterios_evaluacion.md; novedad vacía cuenta como 2."""
    if row['dragon'] == '':
        return ''
    scores = [int(row[name] or 2) for name in CRITERIA]
    total = sum(scores)
    if min(scores) > 0 and scores[0] == 2 and total >= 9:
        return 'aceptar'
    if min(scores) > 0 and total >= 7:
        return 'reserva'
    return 'descartar'


def decide(table):
    # utf-8-sig: Excel guarda los CSV con BOM.
    with table.open(encoding='utf-8-sig', newline='') as source:
        rows = list(csv.DictReader(source))
    for row in rows:
        row['decision'] = decision(row)
    with table.open('w', encoding='utf-8', newline='') as target:
        writer = csv.DictWriter(target, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row['decision'] or 'sin evaluar' for row in rows)
    for name, count in counts.items():
        print(f'{name}: {count} de {len(rows)}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidates', type=Path, help='Carpeta con PNG y manifest.json.')
    parser.add_argument('--output', type=Path, default=Path('docs/data/evaluacion_candidatos.csv'))
    parser.add_argument('--decide', type=Path, help='Tabla ya evaluada para calcular decisiones.')
    args = parser.parse_args()
    if args.decide:
        decide(args.decide)
    else:
        create(args.candidates, args.output)


if __name__ == '__main__':
    main()
