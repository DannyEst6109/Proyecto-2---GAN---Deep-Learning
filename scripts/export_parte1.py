"""Empaqueta evidencias de la parte 1 sin modificar el repositorio ni publicar."""

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import torch

ROOT = Path(__file__).resolve().parents[1]


def export(runs, candidates, output):
    runs, candidates, output = Path(runs), Path(candidates), Path(output)
    if output.exists():
        raise FileExistsError('Usar un ZIP nuevo para preservar entregas anteriores.')
    report = json.loads((runs / 'report/summary.json').read_text(encoding='utf-8'))
    if not report['all_epochs_completed']:
        raise ValueError('Faltan épocas de las comparaciones.')
    manifest = json.loads((candidates / 'manifest.json').read_text(encoding='utf-8'))
    files = {}
    for name in ('base', 'loss', 'stabilization'):
        checkpoint = torch.load(runs / name / 'last.pt', weights_only=True, map_location='cpu')
        if checkpoint['epoch'] != report['epochs_completed']:
            raise ValueError(f'{name}: checkpoint e informe no coinciden.')
    for path in runs.rglob('*'):
        if path.is_file() and path.suffix != '.tmp':
            files['experiments/' + path.relative_to(runs).as_posix()] = path
    for path in candidates.rglob('*'):
        if path.is_file():
            files['candidates/' + path.relative_to(candidates).as_posix()] = path
    documentation = ['README.md', 'requirements.txt', 'configs/fullbody_v2.json',
                     'docs/entrenamiento_fullbody_v2.md', 'docs/resultados_fullbody_v2.md',
                     'docs/arquitectura_fullbody_v2.md', 'docs/parte_1.md',
                     'docs/data/curation_fullbody_v2.csv', 'docs/data/fullbody_manifest_v2.json',
                     'docs/data/fullbody_result_v2.json', 'docs/data/regeneration_fullbody_v2.json',
                     'docs/data/candidate_review_base_v2.csv', 'docs/data/candidate_review_loss_v2.csv',
                     'docs/data/candidate_review_stabilization_v2.csv']
    for name in documentation:
        path = ROOT / name
        if not path.exists():
            raise FileNotFoundError(f'Documentación pendiente: {name}')
        files['project/' + name] = path
    for folder in ('dragon_gan', 'scripts', 'docs/hypotheses'):
        for path in (ROOT / folder).rglob('*'):
            if path.is_file() and path.suffix in ('.py', '.txt'):
                files['project/' + path.relative_to(ROOT).as_posix()] = path
    matched = []
    for name, path in files.items():
        if name.endswith('/last.pt'):
            with path.open('rb') as source:
                if hashlib.file_digest(source, 'sha256').hexdigest() == manifest['checkpoint_sha256']:
                    matched.append(path)
    if len(matched) != 1:
        raise ValueError('Los candidatos deben proceder de uno de los checkpoints exportados.')
    delivery = {'status': 'parte1_evidence_candidates_pending_team_evaluation',
                'candidate_count': len(manifest['characters']),
                'source_generated_count': manifest['source_generated_count'],
                'selected_final_characters': None,
                'model_selected_for_final_gallery': report.get('selected_model'),
                'experiment_candidate_counts': {
                    name: len(json.loads((runs / f'candidates_{name}/manifest.json').read_text(encoding='utf-8'))['characters'])
                    for name in ('base', 'loss', 'stabilization')
                    if (runs / f'candidates_{name}/manifest.json').exists()},
                'pending': ['Conseguir candidatos reconocibles si el análisis señala fallo de calidad',
                            'Evaluación de candidatos', 'Vecinos más cercanos',
                            'Selección conjunta de diez personajes defendibles y reflexión',
                            'Presentación y matriz final de evidencias'],
                'sha256': {name: hashlib.sha256(path.read_bytes()).hexdigest()
                           for name, path in files.items()}}
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, path in files.items():
            archive.write(path, name)
        archive.writestr('delivery_manifest.json', json.dumps(delivery, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(output) as archive:
        damaged = archive.testzip()
        if damaged:
            raise ValueError(f'ZIP dañado: {damaged}')
    print(f'Entrega local verificada: {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', required=True)
    parser.add_argument('--candidates', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    export(args.runs, args.candidates, args.output)


if __name__ == '__main__':
    main()
