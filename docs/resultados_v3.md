# Resultados de la parte 1, v3 (956 dragones, GPU T4)

Ejecución del 11 de octubre de 2026 en Google Colab (Tesla T4, PyTorch 2.11.0+cu130),
commit `2d615db`, configuración `configs/final_v4.json`, hipótesis `docs/hypotheses/v3/`.
600 épocas por variante (≈9 600 actualizaciones), unos 2 s por época con guardado en Drive.
Resultados en `MyDrive/proyecto2_gan/runs/final_v3` y en `parte1_v3_base_450.zip`.

## Resumen numérico (promedio de las últimas 50 épocas)

| Variante | D(real) | D(fake) | Pérdida D | Desv. pérdida G | Épocas con pérdida D < 0,05 |
|---|---:|---:|---:|---:|---:|
| base (no saturante) | 0,9515 | 0,0490 | 0,1065 | 0,5549 | 268 |
| loss (minimax) | 0,9825 | 0,0174 | 0,0396 | 0,0148 | 554 |
| stabilization (normalización espectral) | 0,9446 | 0,5223 | 0,4012 | 0,0141 | 0 |

Diversidad del ruido fijo (distancia media entre las 16 muestras; cerca de 0 = colapso):
base sube de 0,37 (época 50) a un máximo de 0,74 (época 200) y queda en ~0,6;
stabilization cae de 0,26 (época 50) a 0,03 (época 300 en adelante).

## Interpretación

**Base.** Es la única variante que produce dragones reconocibles: siluetas con alas,
cuernos y púas, en varios colores y poses, sin colapso entre las 16 posiciones de ruido fijo.
D domina gran parte del entrenamiento (268 épocas con pérdida de D < 0,05), pero
la pérdida no saturante mantiene gradiente útil y la imagen sigue mejorando hasta
la época ~450. Entre 450 y 600 las muestras cambian poco.

**Pérdida: hipótesis confirmada.** Con minimax, D llega casi enseguida a pérdida ~0
y la pérdida de G se queda en ~0: es la saturación que predice la teoría (log(1 − D(G(z)))
no aporta gradiente cuando D rechaza con confianza). G solo produce texturas repetidas.
Hubo un breve repunte en la época 531 (G = −0,58, D = 1,10) que volvió a saturarse.

**Estabilización: hipótesis rechazada.** La normalización espectral sí evitó que D
dominara (0 épocas con pérdida de D < 0,05; D(fake) ≈ 0,52), pero G colapsó: las 16 muestras
convergen a la misma mancha gris y la diversidad cae a 0,03. Unas curvas "equilibradas"
no implicaron un entrenamiento sano: D quedó demasiado restringido (sin BatchNorm y con
la misma tasa de aprendizaje que G) para dar una señal informativa. Probar una tasa de
aprendizaje mayor para D (TTUR) o conservar BatchNorm serían los siguientes experimentos.

## Modelo elegido

Base, snapshot de la **época 450**
(`runs/final_v3/base/snapshots/generator_epoch_0450.pt`): calidad visual similar a la
época 600 y algo más de diversidad. Se generaron 200 candidatos (semillas 1000–1199),
que son el denominador de la tasa de selección.

## Limitaciones

- Una sola semilla por variante.
- A 64×64 los detalles anatómicos (patas, ojos) son borrosos, y muchas formas son abstractas.
- El dataset de entrada es sintético (Stable Diffusion) y de estilos mezclados.
- La métrica de diversidad es auxiliar: no mide calidad ni novedad, que se evalúan
  con la revisión visual y la prueba de vecinos más cercanos.
