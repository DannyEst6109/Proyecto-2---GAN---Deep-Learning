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

1. **Prefiltro automático** (`scripts/rank_candidates.py`): se ordenan los
   2 000 por la distancia de sus características ResNet-18 a la imagen real más
   cercana. Los más cercanos se parecen más a un dragón real. Resultado en
   `docs/data/prefiltro_candidatos.csv`.
2. **Revisión visual** de los 400 primeros en hojas de contacto.
3. **Nota individual** con los seis criterios a los 36 mejores, ampliados.
4. **Vecinos más cercanos** de los preseleccionados para la nota de novedad.

## Resultado

| Decisión | Cantidad | Descripción |
|---|---:|---|
| aceptar | 4 | Dragón claro: cabeza con hocico o cuerpo completo |
| reserva | 32 | Silueta de criatura con cabeza y cuerpo o alas distinguibles |
| descartar | 365 | Silueta parcial o textura, sin cabeza ni extremidades definidas |
| sin revisar | 1 599 | Fuera de los 400 primeros del prefiltro |

Los 365 descartados recibieron la misma nota en grupo. Se evaluaron 401 y no
400 porque un candidato de la primera ronda quedó fuera del prefiltro.

## Selección

Los diez finales son los 4 aceptados más 6 de la reserva, elegidos por mayor
nota y por variedad de pose y paleta. De la reserva se dejaron fuera los que
repetían a otro (por ejemplo `dragon_1587`, parecido a `dragon_0630`).
Motivo de cada uno: `galeria/registro_seleccion.csv`.

**Tasa de selección: 10 ÷ 2 000 × 100 = 0,5 %.**

Seguimos declarando el límite del modelo: solo 4 de 2 000 son dragones claros;
los otros 6 personajes son siluetas reconocibles pero con anatomía incompleta.

## Comparación entre experimentos

Mismas 16 posiciones de ruido fijo (`docs/img/v3_ruido_fijo_variantes.png`):

| Variante | Muestras con silueta (época 450) | Repetición | Primeras formas |
|---|---:|---|---|
| base (no saturante) | 16 de 16 con trazos, unas 5 con silueta | Sin repetición evidente | Época 150 |
| loss (minimax) | 0 de 16 | Todas son el mismo patrón de tablero | Nunca |
| stabilization (norm. espectral) | 0 de 16 | Colapso: 16 manchas grises iguales | Nunca |

## Limitaciones

- Evaluación visual hecha sobre imágenes de 64×64 ampliadas.
- El prefiltro favorece a los candidatos parecidos a imágenes reales; por eso
  la prueba de vecinos se aplica después a los elegidos.
- 1 599 candidatos no se revisaron uno por uno.
- Los nombres y clases de los personajes los puso el equipo, no el modelo.
