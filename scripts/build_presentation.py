"""Genera presentacion.pptx a partir de docs/presentacion_guion.md."""

import argparse
import re
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt


def read_slides(script):
    """'## título' abre una diapositiva; '- ' viñeta, '| a | b |' fila de tabla, '![](ruta)' imagen."""
    slides = []
    for line in script.read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):
            slides.append({'title': line[3:], 'bullets': [], 'rows': [], 'image': None})
        elif slides and line.startswith('- '):
            slides[-1]['bullets'].append(line[2:])
        elif slides and line.startswith('|'):
            slides[-1]['rows'].append([cell.strip() for cell in line.strip('|').split('|')])
        elif slides and (match := re.match(r'!\[.*\]\((.+)\)', line)):
            slides[-1]['image'] = script.parent / match.group(1)
    return slides


def add_picture(slide, path, left, top, width, height):
    """Ajusta la imagen dentro del recuadro sin deformarla."""
    with Image.open(path) as picture:
        ratio = picture.width / picture.height
    if ratio > width / height:
        slide.shapes.add_picture(str(path), left, top, width=width)
    else:
        slide.shapes.add_picture(str(path), left, top, height=height)


def add_table(slide, rows):
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(0.4), Inches(1.4), Inches(12.5), Inches(5.6))
    for width, column in zip((3.4, 0.9, 4.4, 3.8), shape.table.columns):
        column.width = Inches(width)
    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            cell = shape.table.cell(i, j)
            cell.text = text
            cell.text_frame.paragraphs[0].font.size = Pt(13)


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
        title = slide.shapes.title
        title.left, title.top, title.width, title.height = Inches(0.4), Inches(0.2), Inches(12.5), Inches(1)
        title.text = content['title']
        title.text_frame.paragraphs[0].font.size = Pt(30)
        if content['rows']:
            add_table(slide, content['rows'])
            continue
        image = content['image'] if content['image'] and content['image'].exists() else None
        wide = False
        if image:
            with Image.open(image) as picture:
                wide = picture.width > 2 * picture.height
        # Imagen ancha: abajo a todo el ancho. Imagen normal: a la derecha.
        width, height = (12.3, 2.9) if wide else (6.2, 5.6) if image else (12.3, 5.6)
        frame = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(width), Inches(height)).text_frame
        frame.word_wrap = True
        for index, bullet in enumerate(content['bullets']):
            paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
            paragraph.text = '• ' + bullet
            paragraph.font.size = Pt(15 if image else 18)
            paragraph.space_after = Pt(6)
        if wide:
            add_picture(slide, image, Inches(0.5), Inches(4.4), Inches(12.3), Inches(2.9))
        elif image:
            add_picture(slide, image, Inches(7), Inches(1.3), Inches(5.9), Inches(5.9))
    deck.save(args.output)

    main_slides = sum(not content['title'].startswith('Anexo') for content in slides)
    print(f'{args.output}: {main_slides} diapositivas y {len(slides) - main_slides} anexos.')
    if main_slides > 12:
        print('AVISO: el máximo es 12 diapositivas sin contar anexos.')


if __name__ == '__main__':
    main()
