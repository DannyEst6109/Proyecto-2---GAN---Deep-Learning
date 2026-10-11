# Proyecto 2: dragones generados con GAN

Universo propuesto: dragones de fantasía medieval con escamas, cuernos y alas.
Game of Thrones es una referencia visual; los personajes finales deben ser nuevos.
Se admiten retratos y cuerpos completos (v3); v2 se limitó a cuerpo completo.

## Estado

- **v2 (22 imágenes, CPU):** las tres variantes colapsaron; se conserva como evidencia
  de colapso de modos. Ver `docs/resultados_fullbody_v2.md`.
- **v3 (965 imágenes, GPU):** código, datos, configuración e hipótesis listos y
  probados de punta a punta. Falta ejecutar el entrenamiento en Colab con
  `output/jupyter-notebook/parte_1_gan.ipynb`. Ver `docs/entrenamiento_v3.md`.

Entorno local: desarrollo y ejecución con CPU, compartiendo código por GitHub.
Entrenamiento v3: Google Colab con GPU T4 (en CPU cada época tarda ~30 s).

## División

- Parte 1: GAN, entrenamiento, checkpoints, experimentos de pérdida y estabilización,
  registros de pérdidas y ruido fijo, generación y regeneración.
- Persona 2: dataset y permisos, preparación de imágenes, vecinos más cercanos,
  evaluación, selección de galería y organización del PDF.
- Ambos: universo, interpretación de resultados, selección del modelo y revisión final.

## Inicio de la parte 1

Consultar `docs/trabajo_local.md` para configurar el entorno y colaborar por GitHub.
Abrir `output/jupyter-notebook/parte_1_gan.ipynb` en JupyterLab local.
El entrenamiento usa PyTorch con CPU o GPU compatible; sus versiones efectivas deben
registrarse en cada ejecución. El entorno local se comprobó con Python 3.13.7,
PyTorch 2.14.1+cpu y torchvision 0.29.1+cpu; instalación en `requirements.txt`.
La comprobación de cómputo y retropropagación pasó en CPU. La selección del piloto
tiene procedencia sintética; no equivale a completar el entrenamiento del proyecto.

La configuración inicial está en `configs/base.json`. Sus valores son propuestas,
no valores optimizados. Deben fijarse antes de comenzar las comparaciones.
La semilla propuesta es 42. Ver `docs/experimentos.md` y
`docs/entrega_dataset.md` antes de entrenar.

## Entrega final pendiente

- Código ejecutable y versiones de dependencias.
- Pesos finales o enlace para descargarlos.
- Galería de al menos 10 PNG con semillas o vectores z y tasa de selección.
- Evidencias de ruido fijo, pérdidas interpretadas y vecinos más cercanos.
- `presentacion.pdf`: máximo 12 diapositivas y anexos opcionales.
- Matriz de evidencias, reflexión final y limitaciones.

## Uso de asistentes de IA

Se utilizó Claude (Claude Code) para revisar el proyecto, diagnosticar el colapso de v2,
implementar los cambios de v3 (datos completos, volteo, normalización espectral,
snapshots, caché de imágenes) y preparar el notebook de Colab.
Se utilizó Codex para analizar las instrucciones, distribuir responsabilidades
y preparar la estructura, el plan de experimentos y el código de modelo,
entrenamiento, generación, búsqueda y curación asistida del dataset y pruebas técnicas
con datos sintéticos. La curación requiere revisión del equipo.
Actualizar esta declaración conforme se utilice asistencia adicional.
Las imágenes finales deben provenir exclusivamente de la GAN entrenada por el equipo.
