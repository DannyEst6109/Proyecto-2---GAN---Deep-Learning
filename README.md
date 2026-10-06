# Proyecto 2: dragones generados con GAN

Universo propuesto: dragones de fantasía medieval con escamas, cuernos y alas.
Game of Thrones es una referencia visual; los personajes finales deben ser nuevos.
Encuadre acordado: cuerpo completo, con alas y anatomía visibles.
El estilo definitivo se ajustará según los datos disponibles.

## Estado

Preparación inicial. No hay dataset, modelo implementado, pesos ni resultados.
Modalidad acordada: desarrollo y ejecución local, compartiendo código por GitHub.
En este equipo se detectó Intel Graphics; se utilizará CPU inicialmente.
Cada integrante debe comprobar por separado el hardware de su computadora.
El notebook inicial comprueba la configuración y registra el plan; no entrena todavía.

## División

- Persona 1: GAN, entrenamiento, checkpoints, experimentos de pérdida y estabilización,
  registros de pérdidas y ruido fijo, generación y regeneración.
- Persona 2: dataset y permisos, preparación de imágenes, vecinos más cercanos,
  evaluación, selección de galería y organización del PDF.
- Ambos: universo, interpretación de resultados, selección del modelo y revisión final.

## Inicio de la persona 1

Consultar `docs/trabajo_local.md` para configurar el entorno y colaborar por GitHub.
Abrir `output/jupyter-notebook/persona_1_gan.ipynb` en JupyterLab local.
Por ahora utiliza solo la biblioteca estándar de Python.
El entrenamiento posterior usará PyTorch con CPU o GPU compatible; sus versiones efectivas deben
registrarse en cada ejecución. El entorno local se comprobó con Python 3.13.7,
PyTorch 2.14.1+cpu y torchvision 0.29.1+cpu; instalación en `requirements.txt`.
La comprobación de cómputo y retropropagación pasó en CPU. La GAN aún no se ha ejecutado.

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

Se utilizó Codex para analizar las instrucciones, distribuir responsabilidades
y preparar la estructura y el plan inicial de experimentos.
Actualizar esta declaración conforme se utilice asistencia adicional.
Las imágenes finales deben provenir exclusivamente de la GAN entrenada por el equipo.
