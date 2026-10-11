# Búsqueda de dataset de dragones

Consulta: 5 de octubre de 2026. Investigación local; sin commits ni subidas.

## Candidato principal: Dino or Dragon? (Generated)

- Autor/publicador: agrigorev; el código de generación corresponde a Alexey Grigorev.
- Página: https://www.kaggle.com/datasets/agrigorev/dino-or-dragon
- Metadatos: https://www.kaggle.com/api/v1/datasets/view/agrigorev/dino-or-dragon
- Código de origen: https://github.com/alexeygrigorev/dino-or-dragon
- Licencia publicada por Kaggle: CC0: Public Domain.
- Versión consultada: 1.
- Tamaño indicado por los metadatos: aproximadamente 109 MB.
- Contiene clases de dinosaurios y dragones: solo considerar la clase dragon.
- Origen sintético: Stable Diffusion v1.4. No son fotogramas de Game of Thrones.
- ZIP descargado y contenido confirmado: 767 imágenes en `train/dragon` y
  198 en `test/dragon`; además contiene 827 y 196 dinosaurios respectivamente.
- Copia local: `data/raw/dino_or_dragon/dataset-v1.zip`, excluida de Git.
- Metadatos originales: `data/raw/dino_or_dragon/metadata.json`.
- Inspección técnica: `data/raw/dino_or_dragon/inspection.json`.
- Muestra aleatoria de 16 imágenes de entrenamiento, semilla 42:
  `data/raw/dino_or_dragon/review_sample.png` y listado de nombres en JSON.
- El prompt documentado de dragones es `a picture of a dragon`: no garantiza
  cuerpo completo, alas visibles, encuadre consistente ni anatomía correcta.

Es un candidato, no un dataset de entrenamiento aprobado automáticamente.
Revisar imágenes, encuadres, estilo y duplicados antes de cerrar la selección.
No mezclar las carpetas de dinosaurios con las de dragones.

La muestra inspeccionada mezcla primeros planos, cuerpos completos, dibujos
y apariencia tridimensional, con fondos variados. No cumple automáticamente
nuestro criterio de cuerpo completo y estilo consistente; requiere curación.
La revisión completa dejó seis imágenes para un piloto técnico en `data/dragons`.
Este candidato no se aprueba como dataset final de cuerpo completo por falta de
imágenes adecuadas. Ver `docs/dataset_piloto.md` y el registro de curación.

Descarga reproducible de la versión consultada:
https://www.kaggle.com/api/v1/datasets/download/agrigorev/dino-or-dragon?datasetVersionNumber=1

El PDF exige que las imágenes finales provengan de la GAN entrenada por la pareja.
No especifica expresamente si admite imágenes sintéticas en el dataset de entrada.
Esta distinción y el origen sintético deben declararse; no presentar las imágenes
descargadas como resultados de nuestra GAN ni como material original de la serie.

## Otros candidatos revisados

### Dragon artwork (images.cv)

https://images.cv/dataset/dragon-artwork-image-classification-dataset

La página anuncia 183 imágenes y descarga gratuita. Indica revisar la licencia
de las fuentes, pero no se verificó permiso por imagen. No se recomienda como
dataset definitivo con la información disponible. Tampoco se verificó que todas
las imágenes sean de cuerpo completo.

### Dragon Dataset (thepycoder)

https://github.com/thepycoder/dragon_data

El README indica unas 100 imágenes descargables desde URLs en anotaciones.
No se verificó una licencia de imágenes suficiente para documentar el uso.
No seleccionado para entrenamiento.

### 3 Dragon Animation Pack (OpenGameArt)

https://opengameart.org/content/3-dragon-animation-pack

Autor: GreatDog_ARt. Licencia publicada: CC0. Solo tres diseños animados:
los fotogramas no representan cientos de personajes distintos. Insuficiente
como única fuente para sostener la diversidad de diez personajes nuevos.

## Descartes

- `lesc-unifi/dragon`: DRAGON es el nombre de un dataset de detección de imágenes
  sintéticas de temas generales, no de criaturas dragón.
- `avfattakhova/dragon_dataset`: dataset de texto, no de imágenes.
- Chimera Painter: sus imágenes de entrenamiento representan 30 tipos de animales;
  los ejemplos de híbridos son mapas de segmentación. No es un dataset directo de dragones.

## Próxima preparación

1. Revisar el candidato principal visualmente, conservando los originales.
2. Seleccionar dragones completos con un estilo y fondo razonablemente consistentes.
3. Mantener por separado la partición de prueba para revisión adicional.
4. Documentar cantidad antes/después, motivos de descarte, fuentes, licencia y origen sintético.
5. Crear la versión de entrenamiento y su manifiesto con hashes antes del piloto.
