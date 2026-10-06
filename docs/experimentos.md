# Plan de experimentos de persona 1

Plan propuesto; todavía no ejecutado. Ajustar el presupuesto con una prueba corta
y luego fijar la configuración para todos los experimentos comparables.

## Configuración base

DCGAN de 64×64, pérdida no saturante del generador y discriminador binario.
Los parámetros iniciales están en `configs/base.json`.

## Experimento de pérdida

Comparar la base con la pérdida minimax original del generador. Mantener la misma
pérdida del discriminador y todos los demás parámetros.

Hipótesis previa propuesta: creemos que la pérdida no saturante mejorará el
aprendizaje inicial frente a minimax porque proporciona una señal más útil cuando
el discriminador rechaza las muestras del generador. Lo consideraremos útil si,
con el mismo presupuesto, las muestras de ruido fijo muestran dragones más
reconocibles sin una reducción visible de diversidad.

No comparar directamente las magnitudes de dos pérdidas de generador diferentes
como si fueran una única medida de calidad. Analizar también las imágenes y fallos.

## Experimento de estabilización

Comparar la base con ruido gaussiano en las entradas reales y generadas del
discriminador, con desviación estándar propuesta de 0.05 en la escala [-1, 1].
La única modificación experimental será ese ruido; la pérdida seguirá siendo
no saturante. El ruido no se aplica al generar la galería.

Hipótesis previa propuesta: creemos que el ruido de entrada mejorará la estabilidad
porque dificulta que el discriminador separe las imágenes usando diferencias muy
finas. Lo consideraremos útil si reduce episodios de dominio del discriminador
y conserva o mejora la diversidad y coherencia visual del ruido fijo.

## Controles y registros

- Mismos datos, semilla, épocas, arquitectura, optimizadores y ruido de evaluación.
- Reiniciar cada variante desde la misma inicialización; no continuar desde la base.
- Guardar la hipótesis antes de ejecutar y registrar la configuración efectiva.
- Guardar ruido fijo, pérdidas, muestras por época, pesos y estados de optimizadores.
- Los checkpoints deben conservar el estado aleatorio necesario para reanudar.
- Registrar problemas, interrupciones, cambios y resultados, aunque sean negativos.
- Si se ajusta la base después de comparar, repetir las comparaciones afectadas.

## Entrega a persona 2

Por ejecución: configuración, hipótesis, pérdidas, rejillas con ruido fijo,
checkpoint y notas de fallos. Para la selección final: candidatos, identificadores,
vectores z o semillas, cantidad generada y pesos del modelo elegido.

No declarar novedad solo por apariencia: persona 2 realizará la prueba de vecinos
más cercanos y ambos interpretarán los casos dudosos.
