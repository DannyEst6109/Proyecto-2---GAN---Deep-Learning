# Ficha del dataset

## Fuente

| Campo | Valor |
|---|---|
| Nombre | Dino or Dragon? |
| Autor | agrigorev (Alexey Grigorev) |
| URL | https://www.kaggle.com/datasets/agrigorev/dino-or-dragon |
| Código de origen | https://github.com/alexeygrigorev/dino-or-dragon |
| Versión | 1 |
| Licencia publicada | CC0: Public Domain |
| Archivo | `dataset-v1.zip`, 109 298 562 bytes |
| SHA-256 del ZIP | `864f8993a88ed784a91bfb3d6d4d95b9fd2ffd64beea3ed6b3f473469f44657f` |
| Fecha de descarga | 5 y 11 de octubre de 2026 (un integrante cada vez, mismo SHA-256) |

No se incorporaron fuentes adicionales.

## Origen de las imágenes

Las imágenes son **sintéticas**: el autor las generó con Stable Diffusion v1.4 usando
el prompt `a picture of a dragon`. No son fotografías, ilustraciones de artistas
ni fotogramas de una serie.

Game of Thrones es solo nuestra referencia visual para el universo (dragones de
fantasía medieval). El dataset no contiene material oficial de la serie.

El enunciado no aclara si se admiten imágenes sintéticas como entrada, por eso
lo declaramos aquí y en la presentación. Los personajes finales salen únicamente
de la GAN entrenada por el equipo.

## Cantidades

| Conjunto | En el ZIP | Aceptadas | Descartadas |
|---|---:|---:|---:|
| `train/dragon` | 767 | 760 | 7 |
| `test/dragon` | 198 | 196 | 2 |
| **Dragones** | **965** | **956** | **9** |
| `train/dinosaur` y `test/dinosaur` | 1 023 | 0 | 1 023 |

Las 1 023 imágenes de dinosaurios se excluyen por no pertenecer al universo.

## Criterios de aceptación

Una imagen se acepta si cumple todo lo siguiente:

1. El archivo abre sin errores y tiene contenido.
2. No es duplicado exacto ni casi duplicado de otra imagen.
3. Muestra un dragón reconocible (retrato o cuerpo completo).
4. No tiene texto ni marco de carta.
5. No es un recorte extremo donde ya no se distingue la criatura.

No se filtra por estilo ni por encuadre: la revisión anterior, que exigía cuerpo
completo, dejó 22 imágenes y la GAN colapsó (`docs/resultados_fullbody_v2.md`).

## Resultado de la revisión

Revisión técnica automática (`scripts/review_dataset.py`) sobre las 965 imágenes:

- Archivos no legibles: 0.
- Duplicados exactos (SHA-256): 0.
- Casi duplicados (huella perceptual dHash, hasta 4 bits de diferencia): 0.
- Imágenes sin contenido: 1 (completamente negra).
- Todas miden 512×512 píxeles.

Revisión visual en diez hojas de contacto de 100 imágenes, con una segunda
mirada ampliada a 25 casos dudosos. Se descartaron 9 imágenes:

| Motivo | Cantidad |
|---|---:|
| Carta de juego con marco y texto | 5 |
| Imagen completamente negra | 1 |
| Primer plano extremo, dragón no reconocible | 1 |
| Cuerpo sin cabeza reconocible | 1 |
| Fotografía de un dibujo sobre una mesa | 1 |

Registros:

- `docs/data/revision_tecnica.csv`: resultado técnico por archivo.
- `docs/data/exclusiones_persona2.csv`: las 9 descartadas con su motivo.
- `docs/data/curation_final_v4.csv`: decisión, ruta y SHA-256 de las 965.

## Imágenes de prueba

La partición `test` de Kaggle sirve para clasificar dinosaurios y dragones. Una
GAN no usa etiquetas ni evaluación supervisada, así que el equipo decidió sumar
sus 196 dragones aceptados al entrenamiento para tener más datos. El CSV conserva
la carpeta de origen (`train/` o `test/`) de cada imagen para poder separarlas.

## Limitaciones

- Las imágenes vienen de otro modelo generativo: heredan sus errores de anatomía
  (patas de más, alas fusionadas, cabezas deformes).
- El estilo es muy variado: dibujos a lápiz, ilustraciones a color y renders.
- Hay retratos y cuerpos completos mezclados.
- 956 imágenes siguen siendo pocas para una GAN.
- La revisión visual es subjetiva y se hizo sobre miniaturas.
