"""Genera presentacion.pptx a partir de docs/presentacion_guion.md."""

import argparse
import re
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt


def read_slides(script):
    """Cada '## título' abre una diapositiva; '- ' son viñetas y '![](ruta)' la imagen."""
    slides = []
    for line in script.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            slides.append({'title': line[3:], 'bullets': [], 'image': None})
        elif slides and line.startswith('- '):
            slides[-1]['bullets'].append(line[2:])
        elif slides and (match := re.match(r'!\[.*\]\((.+)\)', line)):
            slides[-1]['image'] = script.parent / match.group(1)
    return slides


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script', type=Path, default=Path('docs/presentacion_guion.md'))
    parser.add_argument('--output', type=Path, default=Path('presentacion.pptx'))
    args = parser.parse_args()

    deck = Presentation()
    deck.slide_width, deck.slide_height = Inches(13.33), Inches(7.5)
    slides = read_slides(args.script)
    for content in slides:
        slide = deck.slides.add_slide(deck.slide_layouts[5])  # Solo título.
        slide.shapes.title.text = content['title']
        slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(32)
        has_image = content['image'] and content['image'].exists()
        width = Inches(7.3) if has_image else Inches(12.3)
        frame = slide.shapes.add_textbox(Inches(0.5), Inches(1.6), width, Inches(5.5)).text_frame
        frame.word_wrap = True
        for index, bullet in enumerate(content['bullets']):
            paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
            paragraph.text = '• ' + bullet
            paragraph.font.size = Pt(18)
            paragraph.space_after = Pt(8)
        if has_image:
            slide.shapes.add_picture(str(content['image']), Inches(8), Inches(1.7), height=Inches(5))
    deck.save(args.output)

    pending = sum(bullet.startswith('PENDIENTE') for content in slides for bullet in content['bullets'])
    main_slides = sum(not content['title'].startswith('Anexo') for content in slides)
    print(f'{args.output}: {main_slides} diapositivas y {len(slides) - main_slides} anexos.')
    print(f'Líneas pendientes: {pending}')
    if main_slides > 12:
        print('AVISO: el máximo es 12 diapositivas sin contar anexos.')


if __name__ == '__main__':
    main()
