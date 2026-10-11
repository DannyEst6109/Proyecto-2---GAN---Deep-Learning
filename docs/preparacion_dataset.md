# Preparación del dataset para el entrenamiento

Versión cerrada: **v4**, 956 imágenes. Es la misma para los tres experimentos.

| Elemento | Ubicación |
|---|---|
| Carpeta de entrenamiento | `data/dragons_final_v4` (fuera de Git) |
| Listado de archivos con SHA-256 | `docs/data/curation_final_v4.csv` |
| Huella del manifiesto | `ddf0ac89d84492bf39b47817e409dd83d5c3805bc7e6f396c76f8a24201e911e` |
| Muestra después del cargador | `docs/img/muestra_cargador.png` |
| Procedencia y criterios | `docs/ficha_dataset.md` |

La huella es la que calcula `DragonDataset.manifest()` y debe registrarse en
`dataset_manifest_sha256` de la configuración de entrenamiento.

## Reproducir

```powershell
.\.venv\Scripts\python.exe scripts/review_dataset.py --sheets data/review_sheets
.\.venv\Scripts\python.exe scripts/close_dataset.py
.\.venv\Scripts\python.exe scripts/prepare_dataset.py --selection docs/data/curation_final_v4.csv --output data/dragons_final_v4
.\.venv\Scripts\python.exe -m scripts.loader_sample
```

1. `review_dataset.py` revisa legibilidad y duplicados y crea las hojas de contacto.
2. `close_dataset.py` aplica las exclusiones de `docs/data/exclusiones_persona2.csv`.
3. `prepare_dataset.py` copia del ZIP solo las aceptadas, verificando cada SHA-256.
4. `loader_sample.py` carga todo con el cargador de la GAN y guarda la muestra.

## Transformaciones

Los originales no se modifican: se copian tal cual desde el ZIP (JPG, 512×512).
Las transformaciones las hace el cargador `dragon_gan/data.py` al leer:

1. Corrección de orientación EXIF.
2. Conversión a RGB (fondo blanco si hubiera transparencia).
3. Reducción a 64×64 con Lanczos, conservando proporción. Como todas son
   cuadradas, no hay relleno ni recorte.
4. Normalización de [0, 1] a [-1, 1], igual que la salida `tanh` del generador.

Durante el entrenamiento se aplica volteo horizontal aleatorio (p = 0,5),
definido en `configs/final_v3.json` (`augment_hflip`). No hay otros aumentos.

## Comprobación

Resultado de `loader_sample.py` sobre v4:

- 956 imágenes cargadas sin errores.
- Tensor de forma (956, 3, 64, 64) y rango [-1, 1].
- Media por canal: R −0,104, G −0,156, B −0,224.

En la muestra de 64 imágenes los dragones siguen siendo reconocibles a 64×64,
aunque se pierden detalles finos como escamas y garras.

## Diferencia con v3

v3 usaba los 965 dragones sin revisar. v4 quita 9 (5 cartas con texto, 1 imagen
negra, 2 recortes extremos y 1 fotografía de un dibujo). Si se entrena con v4
hay que crear una configuración nueva con la ruta y la huella de esta versión;
si se entrena con v3, los vecinos más cercanos deben buscarse en v3.
