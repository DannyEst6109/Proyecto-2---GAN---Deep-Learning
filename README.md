# Proyecto 2: dragones generados con GAN

Universo propuesto: dragones de fantasía medieval con escamas, cuernos y alas.
Game of Thrones es una referencia visual; los personajes finales deben ser nuevos.
Se admiten retratos y cuerpos completos (v3); v2 se limitó a cuerpo completo.

## Estado

- **v2 (22 imágenes, CPU):** las tres variantes colapsaron; se conserva como evidencia
  de colapso de modos. Ver `docs/resultados_fullbody_v2.md`.
- **v3 (956 imágenes del dataset v4, GPU):** entrenada en Colab. La base genera dragones
  reconocibles; modelo elegido: base, época 450. Ver `docs/resultados_v3.md`.
  Notebook: `output/jupyter-notebook/parte_1_gan.ipynb`; método: `docs/entrenamiento_v3.md`.

Entorno local: desarrollo y ejecución con CPU, compartiendo código por GitHub.
Entrenamiento v3: Google Colab con GPU T4 (en CPU cada época tarda ~30 s).

## División

- Parte 1: GAN, entrenamiento, checkpoints, experimentos de pérdida y estabilización,
  registros de pérdidas y ruido fijo, generación y regeneración.
- Persona 2: dataset y permisos, preparación de imágenes, vecinos más cercanos,
  evaluación, selección de galería y organización del PDF.
- Ambos: universo, interpretación de resultados, selección del modelo y revisión final.

## Cómo ejecutar

Entorno local (Windows, CPU), desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/check_environment.py
```

Entrenamiento: abrir `output/jupyter-notebook/parte_1_gan.ipynb` en Google Colab con
GPU T4 y ejecutar todo. Descarga el dataset, entrena las tres variantes con
`configs/final_v4.json` y genera el informe. Detalle en `docs/entrenamiento_v3.md`.

| Entorno | Uso | Versiones |
|---|---|---|
| Google Colab, Tesla T4 | Entrenamiento de las tres variantes | Python 3.13.15, PyTorch 2.11.0+cu130, NumPy 2.1.3 |
| Windows, CPU | Dataset, candidatos, galería, vecinos y presentación | Python 3.11.8, PyTorch 2.14.1+cpu, torchvision 0.29.1+cpu |

`requirements.txt` fija las versiones verificadas con Python 3.13.7. Con Python 3.11
se usaron las mismas versiones de PyTorch y torchvision, NumPy 2.4.6 y matplotlib 3.8.4.

## Persona 2: dataset, evaluación y presentación

| Tarea | Documento | Código |
|---|---|---|
| Revisión y selección del dataset (v4, 956 imágenes) | `docs/ficha_dataset.md` | `scripts/review_dataset.py`, `scripts/close_dataset.py` |
| Preparación y comprobación con el cargador | `docs/preparacion_dataset.md` | `scripts/loader_sample.py` |
| Criterios y tabla de evaluación | `docs/criterios_evaluacion.md` | `scripts/evaluation_table.py` |
| Vecinos más cercanos | `docs/vecinos_cercanos.md` | `scripts/nearest_neighbors.py` |
| Galería final y tasa de selección | `docs/galeria_final.md` | `scripts/build_gallery.py` |
| Presentación | `docs/presentacion_guion.md` | `scripts/build_presentation.py` |
| Matriz de evidencias | `docs/matriz_evidencias.md` | |

Con los candidatos de la parte 1 (`<candidatos>` = carpeta con PNG y `manifest.json`):

```powershell
.\.venv\Scripts\python.exe scripts/evaluation_table.py --candidates <candidatos>
.\.venv\Scripts\python.exe scripts/evaluation_table.py --decide docs/data/evaluacion_candidatos.csv
.\.venv\Scripts\python.exe scripts/build_gallery.py --candidates <candidatos>
.\.venv\Scripts\python.exe -m scripts.nearest_neighbors --generated galeria --metric cnn
.\.venv\Scripts\python.exe scripts/build_presentation.py
```

Resultado: 2 000 candidatos generados, 10 personajes seleccionados (tasa de
selección del 0,5 %) y ninguno es copia de una imagen de entrenamiento. Se revisaron
los 2 000: 9 son dragones claros y 8 de ellos están en la galería. Ver `docs/evaluacion_candidatos.md`.

## Entrega final

| Entregable | Ubicación |
|---|---|
| Presentación | `presentacion.pdf` (editable: `presentacion.pptx`) |
| Galería de 10 PNG con semillas y vectores z | `galeria/` |
| Pesos del generador elegido (base, época 450) | `pesos/generator_epoch_0450.pt` |
| Código | `dragon_gan/`, `scripts/`, `output/jupyter-notebook/parte_1_gan.ipynb` |
| Matriz de evidencias | `docs/matriz_evidencias.md` y diapositiva 12 |

Regenerar la galería desde los pesos y los vectores z:

```powershell
.\.venv\Scripts\python.exe -m dragon_gan.generate --checkpoint pesos/generator_epoch_0450.pt --output runs/galeria_regenerada --manifest galeria/galeria_selection.json
```

Semillas: 42 para el entrenamiento, 43 para el ruido fijo y 1000–2999 para los
2 000 candidatos. Las de los diez personajes están en `galeria/registro_seleccion.csv`.

## Uso de asistentes de IA

Se utilizó Claude (Claude Code) para revisar el proyecto, diagnosticar el colapso de v2,
implementar los cambios de v3 (datos completos, volteo, normalización espectral,
snapshots, caché de imágenes) y preparar el notebook de Colab.
Se utilizó Codex para analizar las instrucciones, distribuir responsabilidades
y preparar la estructura, el plan de experimentos y el código de modelo,
entrenamiento, generación, búsqueda y curación asistida del dataset y pruebas técnicas
con datos sintéticos. La curación requiere revisión del equipo.
En la parte de persona 2 se utilizó Claude (Claude Code) como apoyo para revisar el
dataset en hojas de contacto, programar los scripts de revisión, evaluación, vecinos
más cercanos y galería, y redactar la documentación. Las decisiones de selección
requieren confirmación del equipo.
Actualizar esta declaración conforme se utilice asistencia adicional.
Las imágenes finales deben provenir exclusivamente de la GAN entrenada por el equipo.
