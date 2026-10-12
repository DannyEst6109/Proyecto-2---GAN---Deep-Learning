# Vecinos más cercanos

Objetivo: comprobar si un personaje generado es casi una copia de una imagen
del entrenamiento. Código: `scripts/nearest_neighbors.py`.

## Método

1. Se cargan las imágenes de entrenamiento con el mismo cargador de la GAN
   (64×64, RGB, rango [-1, 1]).
2. Se agregan sus versiones volteadas, porque el entrenamiento usa volteo
   horizontal y el generador pudo aprender la imagen reflejada.
3. Cada imagen se convierte en un vector según la métrica elegida.
4. Se calcula la distancia (raíz del error cuadrático medio) entre cada
   personaje y todas las imágenes de entrenamiento, y se guardan las 5 menores.

Se usan tres métricas porque cada una falla en casos distintos:

| Métrica | Vector | Detecta | No detecta |
|---|---|---|---|
| `cnn` (principal) | 512 características de ResNet-18 preentrenada en ImageNet | Parecido de contenido y estilo | Depende de lo que aprendió la red con fotos reales |
| `pixel` | Los 12 288 valores RGB | Copias casi exactas | Copias con otro brillo o color |
| `forma` | Grises 16×16 sin brillo ni contraste | Misma silueta con otro color | Copias desplazadas o con zoom |

El enunciado recomienda las características de una CNN preentrenada, por eso
`cnn` es la métrica principal. Las otras dos son comprobaciones simples que no
dependen de ningún modelo externo.

## Referencia para interpretar las distancias

Una distancia sola no dice nada. Por eso se calcula, para cada imagen real, la
distancia a su vecina real más cercana (sin contarse a sí misma). Si un
personaje está más cerca de una imagen de entrenamiento que el 5 % de las
reales entre sí (percentil 5), se marca para revisión.

Con el dataset v4 (956 imágenes):

| Métrica | Percentil 5 | Mediana |
|---|---:|---:|
| `cnn` | 0,240 | 0,302 |
| `pixel` | 0,303 | 0,440 |
| `forma` | 0,768 | 0,981 |

## Prueba del método

Antes de aplicarlo a los personajes se probó con cuatro imágenes de control:

| Control | `cnn` | `pixel` | `forma` | Alerta |
|---|---:|---:|---:|---|
| Copia exacta de una imagen de entrenamiento | 0,000 | 0,000 | 0,000 | En las tres |
| Copia volteada | 0,000 | 0,000 | 0,000 | En las tres, marcada como volteada |
| Copia con 50 % más de brillo | 0,332 | 0,429 | 0,239 | Solo en `forma` |
| Ruido aleatorio | 0,895 | 0,496 | 1,256 | Ninguna |

En los tres primeros casos el vecino número 1 fue la imagen original correcta
con las tres métricas. La copia con brillo muestra por qué no basta el umbral:
hay que mirar siempre la figura con el vecino al lado.

También se observó que imágenes borrosas de un modelo poco entrenado quedan
cerca de muchas reales en `pixel` (porque se parecen al promedio) pero muy
lejos en `cnn` (0,82 a 0,84).

## Uso

```powershell
.\.venv\Scripts\python.exe -m scripts.nearest_neighbors --generated galeria --metric cnn
.\.venv\Scripts\python.exe -m scripts.nearest_neighbors --generated galeria --metric pixel
.\.venv\Scripts\python.exe -m scripts.nearest_neighbors --generated galeria --metric forma
```

`--data` debe apuntar a la carpeta con la que realmente se entrenó el modelo.
Salidas en `docs/vecinos/`: `vecinos_<métrica>.png` con cada personaje junto a
sus vecinas y `vecinos_<métrica>.csv` con archivo, distancia y alerta.

## Limitaciones

- Comparar píxeles no mide parecido semántico: dos dragones con la misma pose
  pero desplazados unos píxeles quedan lejos.
- ResNet-18 se entrenó con fotos reales, no con ilustraciones de dragones; sus
  características pueden ignorar detalles que a una persona le parecen claves.
- A 64×64 se pierden detalles; dos imágenes distintas pueden parecer cercanas.
- El umbral del percentil 5 es una convención nuestra, no una prueba.
- Un personaje puede combinar partes de varias imágenes sin parecerse a ninguna.

Estas comparaciones aportan evidencia sobre semejanza; **por sí solas no
demuestran novedad**.

## Resultados con los diez personajes finales

Figuras: `docs/vecinos/vecinos_cnn.png`, `vecinos_pixel.png` y `vecinos_forma.png`.
Distancia al vecino más cercano de cada personaje (entre paréntesis, el
percentil 5 entre imágenes reales):

| Personaje | `cnn` (0,240) | `pixel` (0,303) | `forma` (0,768) | Alerta |
|---|---:|---:|---:|---|
| 01 Fauce Carmesí | 0,602 | 0,441 | 0,865 | No |
| 02 Ámbar Errante | 0,603 | 0,383 | 0,915 | No |
| 03 Cresta Sombría | 0,596 | 0,449 | 0,929 | No |
| 04 Vela Nocturna | 0,591 | 0,462 | 0,951 | No |
| 05 Brasa Celeste | 0,624 | 0,628 | 0,943 | No |
| 06 Bruma Gris | 0,637 | 0,406 | 1,010 | No |
| 07 Marea Azul | **0,578** | 0,478 | 1,017 | No |
| 08 Llama Dorada | 0,603 | 0,324 | 1,065 | No |
| 09 Garra Sombría | 0,613 | 0,634 | 1,108 | No |
| 10 Paso Viejo | 0,640 | 0,436 | 1,026 | No |

### Interpretación

- **Ningún personaje es copia de una imagen de entrenamiento.** Ninguna de las
  tres métricas da alerta y en las figuras ninguna silueta coincide con la de
  su vecina.
- **Los vecinos comparten color y fondo con el personaje.** Rojo sobre celeste
  para 01, 04 y 05; gris para 06 y 10; azul sobre ocre para 07. El generador
  aprendió las combinaciones de color del dataset.
- **Un mismo dragón real aparece como vecino de varios personajes** (la cabeza
  roja sobre fondo verde azulado, en 01, 02, 03 y 04). Indica que esa zona del
  dataset pesa mucho en lo que el modelo genera.
- **Estar lejos no es solo buena noticia.** En `cnn` los personajes están a
  0,58–0,64 de su vecina, el doble de la mediana entre reales (0,302). No son
  copias, pero tampoco tienen el detalle de un dragón del dataset.

### El personaje más difícil de defender

**07, Marea Azul.** Es el más cercano a una imagen real según ResNet-18
(0,578). Su vecina es un dragón azul enroscado sobre fondo ocre: la misma
paleta, el mismo fondo y una composición circular parecida. La figura no es la
misma —no coinciden cabeza, patas ni contorno, y en `forma` queda por encima
de la mediana entre reales—, pero la idea visual sí viene de esa imagen.

Este caso muestra qué aprendió la GAN: primero lo más fácil y repetido del
dataset —fondos lisos, paletas y trazos de escamas—, y solo parcialmente la
estructura de un dragón. La novedad de nuestros personajes está en la forma;
el color y el fondo están tomados del dataset.

### Primera ronda

Con la galería inicial (10 de 200 candidatos) hubo dos alertas en `pixel` por
fondos pardos casi idénticos a una imagen real. Esa galería se reemplazó al
ampliar a 2 000 candidatos; ver `docs/evaluacion_candidatos.md`.
