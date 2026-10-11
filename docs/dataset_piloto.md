# Curación del dataset y alcance del piloto

Se revisaron las 767 imágenes de `train/dragon` de Dino or Dragon?, versión 1.
Las 198 imágenes de `test/dragon` permanecen en el ZIP original, fuera del entrenamiento.
Se hizo un cribado en 22 hojas de contacto y una segunda revisión ampliada de
36 candidatas. Se conservaron seis imágenes: índices 517, 518, 609, 676, 756 y 762
del listado ordenado de rutas del ZIP. Las otras 761 se descartaron.

El criterio fue una criatura principal, cuerpo y cola dentro del encuadre, alas
visibles e ilustración con color. La revisión es subjetiva: no certifica anatomía
correcta y las seis imágenes conservan variaciones de estilo. No se alteraron ni
recortaron los originales; el cargador reduce a 64×64 y conserva la proporción.

La selección es **solo para una prueba técnica**. Seis imágenes no ofrecen una
base suficiente para defender diversidad y generalización de diez personajes
nuevos. Este candidato no se aprueba como dataset final de cuerpo completo.
Hace falta ampliar las fuentes documentadas o acordar un cambio de encuadre.

## Procedencia y trazabilidad

- Autor/publicador: agrigorev (Alexey Grigorev).
- Fuente: https://www.kaggle.com/datasets/agrigorev/dino-or-dragon
- Código de origen: https://github.com/alexeygrigorev/dino-or-dragon
- Licencia publicada en Kaggle: CC0: Public Domain.
- Origen: imágenes sintéticas de Stable Diffusion v1.4, prompt `a picture of a dragon`.
- No son fotogramas ni personajes oficiales de Game of Thrones.
- ZIP SHA-256: `864f8993a88ed784a91bfb3d6d4d95b9fd2ffd64beea3ed6b3f473469f44657f`.
- Registro de las 767 decisiones y hashes: `docs/data/curation_v1.csv`.
- Manifiesto de las seis seleccionadas: `docs/data/pilot_manifest_v1.json`.

Los motivos de descarte se anotaron agrupados; el CSV no atribuye un diagnóstico
individual a cada imagen. Tanto el PDF como la documentación final deben declarar
el origen sintético; el enunciado no lo admite ni prohíbe expresamente para los datos
de entrada. Los resultados finales deben proceder de la GAN entrenada por el equipo.

## Reproducir en la computadora de la persona 2

Desde la raíz del repositorio, descargar el ZIP original y ejecutar:

```powershell
New-Item -ItemType Directory -Force data/raw/dino_or_dragon
Invoke-WebRequest -Uri 'https://www.kaggle.com/api/v1/datasets/download/agrigorev/dino-or-dragon?datasetVersionNumber=1' -OutFile data/raw/dino_or_dragon/dataset-v1.zip
.\.venv\Scripts\python.exe scripts/prepare_dataset.py
.\.venv\Scripts\python.exe -m dragon_gan.train --config configs/pilot_curated_v1.json --data data/dragons --output runs/pilot_curated_v1 --device cpu --stop-after 1
```

El script verifica el ZIP y cada original antes de copiar. Puede repetirse si los
archivos de destino coinciden; rechaza un destino con contenido diferente.
Las imágenes, el ZIP y los pesos permanecen excluidos de Git. El CSV, los hashes,
el script y la configuración permiten reconstruir la misma selección.

El piloto usa una época, semilla 42, red base de 64×64, cuatro hilos de CPU y un
único lote de seis imágenes (batch_size máximo 64, sin descartar lote incompleto).
Su configuración está separada de `configs/base.json`: no sustituye los experimentos
base, pérdida y estabilización ni proporciona una estimación válida para un dataset mayor.

## Resultado comprobado

El piloto completó la época en CPU sin errores ni pérdidas no finitas. El bucle
de entrenamiento tardó aproximadamente 0,6 segundos; esta medida excluye el inicio
del proceso y no puede extrapolarse directamente a un dataset mayor. Pérdida G:
7,2408; pérdida D: 0,6371. Son valores de una sola actualización, sin tendencia
suficiente para interpretar estabilidad o convergencia.

Se guardaron `last.pt`, `losses.csv`, `losses.png`, configuración, entorno,
manifiesto y muestras de ruido fijo en `runs/pilot_curated_v1`. Las muestras de
la época 1 son prácticamente grises y no muestran dragones reconocibles. No hay
personajes finales ni evidencia de novedad. El resultado técnico y hash del
checkpoint quedan en `docs/data/pilot_result_v1.json`.

Se comprobó también que repetir la preparación conserva exactamente los seis
originales. El trabajo permanece local en `main`, sin commits ni subidas.
