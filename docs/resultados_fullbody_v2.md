# Resultados de la parte 1: dragones de cuerpo completo

## Alcance y trazabilidad

Se amplió la selección de seis a 22 imágenes, manteniendo cuerpo completo y
admitiendo dibujos e ilustraciones en color y monocromas. Procedencia, licencia
publicada, origen sintético y hashes están en `docs/data/fullbody_manifest_v2.json`.
Los criterios y decisiones están en `docs/data/curation_fullbody_v2.csv`.
La revisión fue asistida por Codex y requiere confirmación del equipo.

Las tres variantes de `runs/fullbody_v2` utilizan la configuración congelada
`configs/fullbody_v2.json`: 300 épocas, 22 imágenes, tres lotes por época,
900 actualizaciones por modelo y variante, CPU, cuatro hilos, semilla 42.
La arquitectura y pérdidas están en `docs/arquitectura_fullbody_v2.md`.
Las hipótesis fueron guardadas antes de entrenar. No se partió del benchmark.

## Interpretación

La base aprendió texturas con artefactos repetidos, sin figura de dragón
reconocible en sus muestras de ruido fijo. Su pérdida G creció mientras D separaba
con facilidad los ejemplos reales y generados. La variante minimax mantuvo una
pérdida G cercana a cero, pero eso no implica calidad: su objetivo numérico es
diferente. Las imágenes de esa variante también son texturas sin anatomía reconocible.

La estabilización tampoco produjo dragones reconocibles: se revisaron las cuatro
hojas de contacto de sus 200 candidatos finales. Su curva G presenta picos grandes
en algunas épocas, por lo que no hay evidencia para declarar que el ruido 0.05
resolvió la inestabilidad. Las puntuaciones de D con entradas perturbadas no se
interpretan directamente como una mejora de calidad respecto de entradas sin ruido.

Las tres variantes completaron las 300 épocas y el reporte verificó datos, entorno,
configuraciones de un solo factor, épocas y ruido fijo. Se comprobó además que
los checkpoints contienen los estados finales alineados del generador aleatorio
de entrenamiento y del orden de datos. El resumen numérico está en
`docs/data/fullbody_result_v2.json`.

| Variante | G, época 300 | D, época 300 | D(real) | D(fake) |
|---|---:|---:|---:|---:|
| Base | 6,1556 | 0,0143 | 0,9849 | 0,0132 |
| Minimax | −0,0013 | 0,0016 | 0,9984 | 0,0017 |
| Ruido 0.05 | 5,8010 | 0,0156 | 0,9829 | 0,0138 |

Los valores precisos prevalecen en el CSV y resumen JSON; las puntuaciones no
son métricas independientes de calidad. No se demostró la mejora de reconocimiento
esperada en la comparación de pérdidas ni la mejora de estabilidad/coherencia
esperada con ruido. Esta observación se limita al dataset, semilla y presupuesto usados.

La inspección de pesos y estados del optimizador de la base confirmó cambios
de parámetros y actualizaciones realizadas. El resultado negativo no se debe a
que el modelo haya quedado sin actualizar. No se identificó una causa única del
fallo; el conjunto pequeño, estilos diversos, resolución y equilibrio adversarial
son limitaciones plausibles, no causas demostradas mediante experimentos aislados.

## Diagnóstico separado, no adoptado

Tras observar texturas y dominio de D se ensayó `configs/fullbody_v3.json`,
lr G=0.0005 y lr D=0.00001, durante 80 épocas de una nueva base.
La hipótesis previa está en `docs/hypotheses/diagnostic_v3.txt`; los archivos en
`runs/fullbody_v3_diagnostic`. Cambió el equilibrio de las pérdidas: D(fake) se
acercó a uno, pero las muestras siguieron siendo texturas. No se adoptó esta base
ni se mezcló el diagnóstico con las tres comparaciones controladas.

## Generación y reproducibilidad

Se generaron 200 candidatos por variante, con semillas 1000–1199, vector z y hash
del checkpoint en cada manifiesto. Los nombres deben identificarse junto con
la variante para evitar confundir imágenes con el mismo nombre de archivo.
La revisión visual de hojas de contacto se registra por variante en `docs/data/`.

Se revisaron 600 candidatos en total: cero fueron aceptados como personajes
reconocibles por la revisión asistida. Tasa de selección asistida: 0/600 = 0 %.
No se eligió modelo final ni diez personajes. El equipo debe confirmar esa evaluación.

Los 200 candidatos de la base se regeneraron con sus vectores guardados y se
comprobó igualdad byte a byte de los PNG en el mismo entorno CPU.
La comprobación está en `docs/data/regeneration_fullbody_v2.json`.
Esto verifica reproducción de resultados, no calidad ni novedad de personajes.

## Entrega y requisitos que permanecen pendientes

Los pesos entrenados, configuraciones, pérdidas, ruido fijo, hipótesis y candidatos
son evidencia técnica de la parte 1. Deben conservarse también los resultados
negativos. No corresponde seleccionar diez texturas y presentarlas como personajes.

La entrega académica sigue necesitando candidatos de dragones reconocibles,
selección conjunta de diez, vecinos más cercanos, justificación de novedad,
reflexión y presentación. La parte de código y ejecución puede entregarse para
revisión, pero no se declara terminado el objetivo visual del proyecto.
