# Criterios de evaluación de candidatos

Definidos antes de ver los candidatos del entrenamiento final, para no ajustar
los criterios a los resultados.

## Criterios

Cada candidato recibe una nota de 0 a 2 en cada criterio.

| Columna | Pregunta | 0 | 1 | 2 |
|---|---|---|---|---|
| `dragon` | ¿Se reconoce como dragón? | Textura o mancha | Criatura ambigua | Dragón claro |
| `cuerpo_alas` | ¿Se ven cuerpo y alas? | Nada distinguible | Solo cabeza o silueta parcial | Cabeza y cuerpo o alas |
| `universo` | ¿Encaja en fantasía medieval? | Fuera de estilo | Parcial | Coherente |
| `anatomia` | ¿Tiene deformaciones? | Graves | Leves | Sin problemas visibles |
| `distinto` | ¿Se diferencia de otros candidatos? | Repetido | Parecido a otro | Diseño propio |
| `novedad` | ¿Se diferencia del entrenamiento? | Copia evidente | Se parece a un vecino | Sin parecido claro |

`novedad` se completa después de calcular los vecinos más cercanos
(`docs/vecinos_cercanos.md`); antes de eso se deja vacío.

## Decisión

- **aceptar**: `dragon` = 2, ningún criterio en 0 y suma de al menos 9 de 12.
- **reserva**: `dragon` ≥ 1, ningún criterio en 0 y suma de 7 u 8.
- **descartar**: cualquier otro caso.

Entre los aceptados, los diez finales se eligen por mayor suma y buscando
variedad de color, pose y encuadre. La selección final la confirman ambos
integrantes.

## Tabla

`scripts/evaluation_table.py` crea una tabla vacía con un candidato por fila:

```powershell
.\.venv\Scripts\python.exe scripts/evaluation_table.py --candidates runs/candidates_v3 --output docs/data/evaluacion_candidatos.csv
```

Columnas: `file`, `seed`, los seis criterios, `observaciones` y `decision`.
Después de llenar las notas, el mismo script calcula la decisión y el resumen:

```powershell
.\.venv\Scripts\python.exe scripts/evaluation_table.py --decide docs/data/evaluacion_candidatos.csv
```

## Comparación entre experimentos

Para comparar base, pérdida y estabilización se revisan las mismas 16 posiciones
de ruido fijo en las mismas épocas y se anota por variante:

- Cuántas de las 16 muestras tienen `dragon` ≥ 1.
- Cuántas se repiten entre sí (falta de diversidad o colapso).
- En qué época aparecen las primeras formas reconocibles.

## Limitaciones

- La evaluación es visual y subjetiva; no se calcula FID porque con menos de
  mil imágenes reales la estimación no es fiable.
- A 64×64 es difícil juzgar anatomía fina.
- Parecerse poco a los vecinos no demuestra que un personaje sea nuevo.
