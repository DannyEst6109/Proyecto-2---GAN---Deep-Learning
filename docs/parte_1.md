# Parte 1: preparación, ejecución y entrega

## Estado

La implementación y ejecución de los tres experimentos están completas en la
primera comparación de 300 épocas con 22 imágenes (`fullbody_v2`). Se generaron
600 candidatos, sin dragones reconocibles en la revisión asistida. Hay pesos,
curvas, controles verificados y regeneración exacta de los 200 candidatos de la base.
Falta resolver calidad visual y conseguir personajes finales; no se declara
completa la entrega académica. Ver `docs/resultados_fullbody_v2.md`.
Los seis dragones del piloto anterior se conservan por separado.
La comparación técnica de tres épocas por variante terminó; su interpretación
está en `docs/resultados_piloto_comparativo.md`. Las muestras siguen prácticamente
grises y las hipótesis académicas permanecen inconclusas.

## Decisiones escritas antes del entrenamiento

Las hipótesis están en `docs/hypotheses/base.txt`, `loss.txt` y `stabilization.txt`.
La base usa pérdida no saturante; `loss` cambia solo a minimax; `stabilization`
añade solo ruido gaussiano 0.05 en D. Nunca combinar ambas modificaciones en
estas comparaciones. Si se reformula una hipótesis, hacerlo antes de una nueva
ejecución y conservar el registro anterior.

Cada variante comienza de nuevo con la misma inicialización, semilla, datos,
orden de lotes y vectores de entrenamiento. El ruido de estabilización tiene
un generador independiente. El ruido fijo de evaluación usa semilla 43;
la semilla principal es 42 y la del ruido de entrada es 44.

La configuración base propone 50 épocas, lotes de hasta 64 y cuatro hilos de CPU.
Ese presupuesto todavía debe revisarse con un piloto sobre el dataset definitivo;
no extrapolar el tiempo de seis imágenes. La resolución es 64×64, por lo que las
estructuras pequeñas y detalles de anatomía pueden ser difíciles de representar.

## Cuando persona 2 entregue el dataset

1. Revisar juntos fuentes, licencia, selección, cantidades y muestra visual.
2. Comprobar la carga a 64×64 y registrar la versión de datos.
3. Medir una época con esos datos. Acordar el presupuesto de las tres ejecuciones.
4. Congelar una configuración nueva; no sobrescribir la de un entrenamiento anterior.
5. Ejecutar la comparación y generar el informe.
6. Interpretar las imágenes y curvas con persona 2 antes de elegir un modelo.

Ejemplo para crear una configuración congelada, desde la raíz del repositorio
y después de ajustar `configs/base.json` al presupuesto acordado:

```powershell
@'
import json
from pathlib import Path
from dragon_gan.data import DragonDataset
config = json.loads(Path('configs/base.json').read_text(encoding='utf-8'))
config['dataset_path'] = 'data/dragons'
config['dataset_manifest_sha256'] = DragonDataset('data/dragons').manifest()[1]
with Path('configs/final_v1.json').open('x', encoding='utf-8') as output:
    json.dump(config, output, indent=2)
'@ | .\.venv\Scripts\python.exe -X utf8 -
```

`final_v1.json` no existe todavía porque aún no se cerró el dataset definitivo.
El nombre por sí solo no aprueba los datos. El ejecutor identifica la selección
actual como piloto y rechaza etiquetarla como resultados del proyecto.

```powershell
.\.venv\Scripts\python.exe -m scripts.run_experiments --config configs/final_v1.json --data data/dragons --output runs/final_v1 --device cpu --purpose project --dry-run
.\.venv\Scripts\python.exe -m scripts.run_experiments --config configs/final_v1.json --data data/dragons --output runs/final_v1 --device cpu --purpose project
.\.venv\Scripts\python.exe -m scripts.compare_experiments --runs runs/final_v1 --output runs/final_v1/report
```

`--dry-run` verifica la huella e imprime el plan sin entrenar ni crear resultados.
Se conserva el plan con hipótesis y hashes del código antes de entrenar. El informe
verifica datos, entorno, configuraciones de un solo factor, épocas, ruido fijo y
muestras iniciales. Produce curvas comparativas, imágenes de las mismas épocas
y una ficha de interpretación. No elige automáticamente un modelo ni declara novedad.

## Interrupciones y reanudación

```powershell
.\.venv\Scripts\python.exe -m scripts.run_experiments --config configs/final_v1.json --data data/dragons --output runs/final_v1 --device cpu --purpose project --resume
```

Se retoma cada variante desde su última época completa. Se exige el mismo plan,
código, configuración, datos, dispositivo e hipótesis; el entrenamiento comprueba
también el entorno. Si una ejecución se interrumpe antes de guardar su primer
checkpoint, conservarla y empezar una comparación nueva en otra carpeta.

Windows puede bloquear temporalmente el reemplazo del checkpoint. Se reintenta
de forma breve sin borrar el checkpoint anterior. Si el bloqueo persiste, el error
se informa; no se considera completada la época sin un guardado correcto.

## Interpretación a completar con resultados definitivos

- Reconocimiento y coherencia: revisar las mismas posiciones del ruido fijo.
- Diversidad: observar si varias posiciones repiten una forma o diseño.
- Pérdidas: relacionar las curvas con cambios visuales; no comparar magnitudes de
  pérdidas de G diferentes como una puntuación de calidad.
- Puntuaciones D(real)/D(fake): describen el entrenamiento; en estabilización se
  calculan sobre entradas con ruido. No miden directamente calidad o novedad.
- Hipótesis: registrar evidencia favorable, contradictoria o inconclusa.
- Modelo elegido: justificar con las imágenes y el análisis, sin elegir por pérdida mínima.
- Limitaciones: una sola semilla, tamaño del dataset, origen sintético y resolución.

## Entrega de la parte 1 a persona 2

Por cada experimento: plan, configuración, hipótesis, entorno, manifiesto de datos,
pesos, pérdidas, rejillas de ruido fijo y notas de interrupciones. Además: figuras
comparativas e interpretación escrita. Conservar el checkpoint elegido en una
ubicación estable; no sobrescribirlo después de generar candidatos.

Después generar los candidatos mediante `dragon_gan.generate`, entregando PNG,
vectores z, semillas y cantidad total. Persona 2 prepara la evaluación y vecinos;
ambos eligen diez. Parte 1 comprueba su regeneración exacta en el mismo entorno.

## Comprobaciones realizadas

El smoke test verifica pérdidas y gradientes finitos, un solo cambio por variante,
alineación de aleatoriedad, reanudación exacta de pesos con y sin ruido, regeneración
idéntica, ejecución conjunta e informe. Rechaza comparaciones con otra semilla y
reanudar con datos modificados. Sus imágenes temporales no son evidencia académica.

No se han creado ramas ni commits. Los cambios permanecen locales en `main`;
coordinar la transferencia de código y metadatos antes de que persona 2 los use.
