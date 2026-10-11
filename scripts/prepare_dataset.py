"""Reproduce la selección visual del piloto desde el ZIP original, sin recortar."""

import argparse
import csv
import hashlib
import io
from pathlib import Path
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA256 = '864f8993a88ed784a91bfb3d6d4d95b9fd2ffd64beea3ed6b3f473469f44657f'


def prepare(archive, selection, output):
    with archive.open('rb') as source:
        archive_hash = hashlib.file_digest(source, 'sha256').hexdigest()
    if archive_hash != ARCHIVE_SHA256:
        raise ValueError('El ZIP no corresponde a la versión 1 documentada.')
    with selection.open(encoding='utf-8', newline='') as source:
        rows = list(csv.DictReader(source))
    accepted = [row for row in rows if row['decision'] in {'aceptar_piloto', 'aceptar_entrenamiento'}]
    if len(accepted) < 2:
        raise ValueError('La selección debe contener al menos dos imágenes.')
    pending = []
    with zipfile.ZipFile(archive) as source:
        for row in accepted:
            member = row['source_path']
            if not member.startswith('train/dragon/') or '..' in Path(member).parts:
                raise ValueError(f'Ruta no autorizada: {member}')
            data = source.read(member)
            if hashlib.sha256(data).hexdigest() != row['sha256']:
                raise ValueError(f'Hash incorrecto: {member}')
            with Image.open(io.BytesIO(data)) as picture:
                picture.verify()
            pending.append((Path(member).name, data))
    expected = {name for name, _ in pending}
    if output.exists():
        actual = {p.name for p in output.iterdir()}
        if actual != expected or any((output / name).read_bytes() != data for name, data in pending):
            raise ValueError('Destino ocupado por datos diferentes; usar otra carpeta vacía.')
    else:
        output.mkdir(parents=True)
        for name, data in pending:
            (output / name).write_bytes(data)
    print(f'{len(pending)} originales verificados: {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=ROOT / 'data/raw/dino_or_dragon/dataset-v1.zip')
    parser.add_argument('--selection', type=Path, default=ROOT / 'docs/data/curation_v1.csv')
    parser.add_argument('--output', type=Path, default=ROOT / 'data/dragons')
    args = parser.parse_args()
    prepare(args.archive, args.selection, args.output)


if __name__ == '__main__':
    main()
