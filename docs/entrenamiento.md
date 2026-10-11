# Parte 1: entrenamiento local

Estado: código implementado y tres variantes de 300 épocas completadas con 22
dragones de cuerpo completo. Se generaron 600 candidatos, sin personajes reconocibles
en la revisión asistida. Ver `docs/entrenamiento_fullbody_v2.md` y
`docs/resultados_fullbody_v2.md`. La galería final sigue pendiente.
La carpeta `data/dragons` conserva el piloto anterior de seis imágenes; la selección
ampliada está en `data/dragons_fullbody_v2`.
Las pruebas con datos sintéticos verifican ejecución y reproducibilidad, no calidad.

## Arquitectura y datos

DCGAN de 64×64: convoluciones transpuestas, BatchNorm, ReLU y salida Tanh en G;
convoluciones, BatchNorm y LeakyReLU en D. D devuelve logits para calcular las
pérdidas con softplus estable. Es una base sencilla para medir cambios aislados.
Referencia: https://docs.pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html

El cargador encuentra PNG/JPG/JPEG/WebP de forma recursiva. Corrige orientación
EXIF, compone transparencia sobre blanco, conserva proporción y añade relleno
blanco hasta 64×64. No recorta alas. Convierte RGB y normaliza a [-1, 1].
Esta preparación es provisional: acordarla con persona 2 para evitar transformaciones
duplicadas. La base no utiliza aumentos aleatorios. Documentar el efecto del relleno.

## Antes de entrenar

1. Obtener y revisar el dataset con su documentación de licencia y fuentes.
2. Colocar únicamente las imágenes aprobadas dentro de `data/dragons/`.
3. Revisar `configs/base.json`: parámetros propuestos, aún no optimizados.
4. Ejecutar una prueba de una época para medir tiempo. Fijar después el presupuesto
   definitivo y volver a comenzar las tres comparaciones con carpetas nuevas.
5. Revisar las hipótesis de `docs/experimentos.md`; pueden reemplazarse mediante
   `--hypothesis-file ruta.txt`, escrito antes del entrenamiento.

Comandos desde la raíz del repositorio, en PowerShell:

```powershell
.\.venv\Scripts\python.exe -m scripts.smoke_test
.\.venv\Scripts\python.exe -m dragon_gan.train --data data/dragons --output runs/pilot --device cpu --stop-after 1
```

El smoke test usa una red pequeña e imágenes sintéticas temporales que elimina;
no produce entregables académicos ni mide el tiempo de la red base con el dataset real.
La prueba `pilot` sí utiliza los datos reales y los parámetros de la base. No utilizar
la ejecución sintética como evidencia de entrenamiento del proyecto.

## Tres ejecuciones controladas

Para la ejecución conjunta con verificación del plan, reanudación y reporte,
seguir `docs/parte_1.md`. Las hipótesis previas tienen archivos separados en
`docs/hypotheses/`. El conjunto actual de seis imágenes sigue siendo solo un piloto.

Tras fijar parámetros y escribir hipótesis, usar la misma configuración para:

```powershell
.\.venv\Scripts\python.exe -m dragon_gan.train --data data/dragons --output runs/base --experiment base --device cpu
.\.venv\Scripts\python.exe -m dragon_gan.train --data data/dragons --output runs/loss --experiment loss --device cpu
.\.venv\Scripts\python.exe -m dragon_gan.train --data data/dragons --output runs/stabilization --experiment stabilization --device cpu
```

- `base`: pérdida no saturante de G, sin ruido de entrada en D.
- `loss`: solo cambia G a minimax original. D conserva su pérdida.
- `stabilization`: solo añade ruido gaussiano de desviación 0.05 a entradas de D.

Cada variante reinicia pesos, semillas y orden de datos desde la misma base.
Usar el mismo equipo, dataset y presupuesto para comparar. No comparar las
magnitudes de pérdidas diferentes de G como si midieran la misma calidad.

## Resultados por ejecución

- `config.json`, `environment.json` y `hypothesis.txt`: registro previo al entrenamiento.
- `dataset_manifest.json`: nombres relativos y hashes; la huella se registra en config.
- `fixed_noise.pt`: mismo ruido de evaluación en todas las variantes.
- `samples/epoch_0000.png` y rejillas de cada época.
- `losses.csv` y `losses.png`: medias por imagen, puntuaciones de D y tiempo por época.
- `last.pt`: pesos de G/D, optimizadores, historial y estados aleatorios al final de cada época.

La huella automática cubre contenido y rutas de imágenes, no permiso de uso.
Persona 2 debe entregar adicionalmente las fuentes y licencias. Si se declara
`dataset_manifest_sha256` en la configuración, debe corresponder a la huella
calculada por este cargador, no al hash de un manifiesto con otro formato.

## Reanudación

```powershell
.\.venv\Scripts\python.exe -m dragon_gan.train --data data/dragons --output runs/base --experiment base --device cpu --resume runs/base/last.pt
```

Se reanuda desde la última época completa. El trabajo de una época interrumpida
se vuelve a ejecutar. Conservar la configuración original y la misma hipótesis
si se utilizó un archivo propio. Se rechazan cambios de datos o configuración.
La reproducibilidad exacta se comprobó en CPU; CUDA no se ha probado aquí.

## Candidatos y regeneración

Cuando el equipo elija un checkpoint real:

```powershell
.\.venv\Scripts\python.exe -m dragon_gan.generate --checkpoint runs/base/last.pt --output runs/candidates --count 200 --seed 1000
```

El manifiesto guarda cada vector z y semilla, cantidad generada y hash del checkpoint.
Las imágenes son candidatos: todavía falta selección, prueba de vecinos y análisis.
Persona 2 puede conservar solo los 10 registros elegidos en una copia del manifiesto,
manteniendo `source_generated_count`, completando `selection_criteria` y cambiando
`status` a `selected`. Guardar ese manifiesto junto con la galería final.

```powershell
.\.venv\Scripts\python.exe -m dragon_gan.generate --checkpoint runs/base/last.pt --output galeria --manifest ruta/al/manifiesto_seleccionado.json
```

La carpeta de salida debe estar vacía. La regeneración usa los vectores guardados
y exige el mismo archivo de pesos. Se verificó igualdad byte a byte de PNG en el
mismo entorno CPU; conservar las versiones para la entrega reproducible.
Conservar el checkpoint seleccionado en una ubicación estable antes de seguir entrenando.
