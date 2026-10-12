# Evaluación de los candidatos

Modelo: base, época 450 (`pesos/generator_epoch_0450.pt`). 200 candidatos,
semillas 1000–1199. Criterios: `docs/criterios_evaluacion.md`, definidos antes
de ver estos resultados. Tabla completa: `docs/data/evaluacion_candidatos.csv`.

## Resultado

| Decisión | Cantidad | Descripción |
|---|---:|---|
| aceptar | 0 | Ningún candidato es un dragón claro (`dragon` = 2) |
| reserva | 12 | Silueta de criatura con cabeza y cuerpo o alas distinguibles |
| descartar (silueta parcial) | 30 | Se intuye una criatura, sin cabeza ni extremidades definidas |
| descartar (textura) | 158 | Colores y trazos de dragón sin figura reconocible |

**Ningún candidato cumple la regla de aceptación.** El generador aprendió la
paleta, los fondos y los trazos de escamas y alas, pero no la anatomía completa
de un dragón. Como la entrega exige diez personajes, los diez se tomaron de los
doce en reserva y se declara aquí que son siluetas, no dragones nítidos.

## Selección

De los doce en reserva se descartaron dos por repetición:

- `dragon_0012` y `dragon_0150`: rojo sobre azul, muy parecidos a `dragon_0152`.

Los diez finales cubren poses y paletas distintas: rojo oscuro, verde azulado,
gris oscuro, naranja, carmesí, violeta, verde dorado, rojo sobre azul, amarillo
y gris monocromo. Motivo de cada uno: `galeria/registro_seleccion.csv`.

**Tasa de selección: 10 ÷ 200 × 100 = 5 %.**

## Comparación entre experimentos

Mismas 16 posiciones de ruido fijo (`docs/img/v3_ruido_fijo_variantes.png`):

| Variante | Muestras con silueta (época 450) | Repetición | Primeras formas |
|---|---:|---|---|
| base (no saturante) | 16 de 16 con trazos, unas 5 con silueta | Sin repetición evidente | Época 150 |
| loss (minimax) | 0 de 16 | Todas son el mismo patrón de tablero | Nunca |
| stabilization (norm. espectral) | 0 de 16 | Colapso: 16 manchas grises iguales | Nunca |

## Limitaciones

- Evaluación visual hecha sobre imágenes de 64×64 ampliadas.
- Las 158 texturas recibieron la misma nota en grupo.
- Los nombres y clases de los personajes son una propuesta creativa del equipo;
  no los produce el modelo.
