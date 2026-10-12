# Evaluación de los candidatos

Modelo: base, época 450 (`pesos/generator_epoch_0450.pt`). 2 000 candidatos,
semillas 1000–2999. Criterios: `docs/criterios_evaluacion.md`, definidos antes
de ver los resultados. Tabla completa: `docs/data/evaluacion_candidatos.csv`.

## Dos rondas

1. **200 candidatos** (semillas 1000–1199, generados en Colab). Ninguno
   alcanzó "aceptar": 12 en reserva y 188 descartados. Eran siluetas abstractas.
2. **2 000 candidatos** (las mismas 200 semillas más 1 800 nuevas). Como el
   modelo no cambia, generar más muestras solo amplía de dónde elegir. Esta es
   la ronda final y la que define la tasa de selección.

## Procedimiento de la ronda final

1. **Orden automático** (`scripts/rank_candidates.py`): se ordenan los 2 000
   por la distancia de sus características ResNet-18 a la imagen real más
   cercana. Resultado en `docs/data/prefiltro_candidatos.csv`.
2. **Revisión visual de los 2 000** en veinte hojas de contacto de 100.
3. **Nota individual** con los seis criterios a los 72 mejores, ampliados.
4. **Vecinos más cercanos** de esos 72 para la nota de novedad.

El orden automático solo sirvió para organizar la revisión. No basta como
filtro: 5 de los 9 aceptados estaban fuera de sus 400 primeros puestos, así
que revisar solo esos habría dejado fuera a los mejores.

## Resultado

| Decisión | Cantidad | Descripción |
|---|---:|---|
| aceptar | 9 | Dragón claro: cabeza con hocico o cuerpo completo |
| reserva | 63 | Silueta de criatura con cabeza y cuerpo o alas distinguibles |
| descartar | 1 928 | Silueta parcial o textura, sin figura reconocible |

Los 1 928 descartados recibieron su nota en grupo, no una por una.
Dos candidatos de la reserva tuvieron alerta de vecinos (`dragon_0033` en
píxeles y `dragon_1390` en forma) y no se consideraron para la galería.

## Selección

Los diez finales son 8 de los 9 aceptados más 2 de la reserva. El aceptado
que quedó fuera (`dragon_0723`) es una cabeza gris muy parecida a
`dragon_0987`. Los dos de reserva (`dragon_1257` y `dragon_0034`) se eligieron
por aportar paletas que no estaban entre los aceptados.
Motivo de cada uno: `galeria/registro_seleccion.csv`.

**Tasa de selección: 10 ÷ 2 000 × 100 = 0,5 %.**

Seguimos declarando el límite del modelo: solo 9 de 2 000 (0,45 %) son
dragones claros, y aun esos tienen anatomía incompleta.

## Comparación entre experimentos

Mismas 16 posiciones de ruido fijo (`docs/img/v3_ruido_fijo_variantes.png`):

| Variante | Muestras con silueta (época 450) | Repetición | Primeras formas |
|---|---:|---|---|
| base (no saturante) | 16 de 16 con trazos, unas 5 con silueta | Sin repetición evidente | Época 150 |
| loss (minimax) | 0 de 16 | Todas son el mismo patrón de tablero | Nunca |
| stabilization (norm. espectral) | 0 de 16 | Colapso: 16 manchas grises iguales | Nunca |

## Limitaciones

- Evaluación visual hecha sobre imágenes de 64×64 ampliadas.
- Los descartados se revisaron en hojas de contacto, con miniaturas de 128 px.
- Los nombres y clases de los personajes los puso el equipo, no el modelo.
