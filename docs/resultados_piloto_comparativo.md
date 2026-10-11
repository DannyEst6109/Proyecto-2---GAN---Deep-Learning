# Comparación técnica: seis dragones, tres épocas

Ejecución completa: `runs/technical_comparison_v2`, CPU, cuatro hilos, semilla 42.
Se usaron `configs/pilot_comparison_v1.json` y las hipótesis escritas previamente
en `docs/hypotheses/`. Cada época contiene un único lote de seis imágenes.
Este ensayo verifica el flujo de experimentos; no sustituye el entrenamiento final.

## Evidencia observada

| Variante | Pérdida G, época 3 | Pérdida D, época 3 | D(real) | D(fake) | Tiempo del bucle, 3 épocas |
|---|---:|---:|---:|---:|---:|
| Base | 7,3995 | 0,0567 | 0,9953 | 0,1013 | 1,34 s |
| Minimax | −0,0010 | 0,0258 | 0,9960 | 0,0455 | 1,06 s |
| Ruido de entrada | 7,3000 | 0,0913 | 0,9911 | 0,1512 | 1,21 s |

Los tiempos excluyen inicio del proceso, figuras y guardado de checkpoints. No
permiten estimar directamente el tiempo de un dataset mayor. Las puntuaciones de
D se registran durante su actualización; en la variante con ruido se usan entradas
perturbadas. No son una evaluación independiente de calidad.

El informe verificó el mismo dataset y entorno, presupuesto, ruido fijo y muestras
iniciales, además de configuraciones con un único factor cambiado. Las pruebas
técnicas adicionales verifican alineación de la secuencia aleatoria de entrenamiento
y reanudación exacta, incluyendo el estado del generador de ruido separado.

## Interpretación visual asistida

Se revisaron `report/fixed_noise_comparison.png` y `report/comparison.png`.
En las épocas 0, 1 y 3, las 16 posiciones del ruido fijo se ven prácticamente
grises en las tres variantes. No hay dragones reconocibles ni detalles suficientes
para evaluar diversidad de personajes. No corresponde declarar colapso del modo
solo a partir de tres actualizaciones y este resultado inicial.

La pérdida de D cae rápidamente y D(real) se acerca a uno, mientras D(fake) cae
al final. Esto es compatible con una separación fácil de los ejemplos durante
este ensayo. No demuestra generalización, convergencia ni calidad de G.

La pérdida minimax cercana a cero no indica que su modelo sea mejor: utiliza un
objetivo distinto. Las diferencias en puntuaciones de la variante con ruido no
bastan para afirmar mayor estabilidad. Ambas hipótesis quedan **inconclusas**.

No se seleccionó modelo ni se generó una galería final. La interpretación requiere
revisión del equipo y debe repetirse con los resultados definitivos.

## Interrupción conservada

`runs/technical_comparison_v1` se interrumpió por un bloqueo de Windows al
reemplazar un checkpoint de la variante minimax. Se conservó la carpeta; no se
incluye como comparación completa. Se añadieron reintentos breves al guardado y
se reiniciaron las tres variantes con el código actualizado en `technical_comparison_v2`.

## Próximo paso académico

Persona 2 revisa y entrega el dataset definitivo con su documentación. Parte 1
mide el tiempo con esos datos, fija presupuesto y hash, ejecuta las tres variantes,
interpreta sus resultados y genera los candidatos. La selección final, vecinos
más cercanos y reflexión requieren resultados reconocibles y revisión conjunta.
