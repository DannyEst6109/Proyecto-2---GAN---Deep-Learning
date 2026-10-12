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
| 01 Ceniza Alta | 0,640 | 0,409 | 0,858 | No |
| 02 Musgo Viejo | 0,652 | 0,345 | 0,910 | No |
| 03 Garra Sombría | 0,660 | 0,425 | 1,127 | No |
| 04 Ámbar Errante | 0,611 | **0,281** | 1,085 | Sí, en `pixel` |
| 05 Fauce Carmesí | 0,596 | 0,459 | 0,985 | No |
| 06 Vela Nocturna | 0,606 | 0,448 | 0,937 | No |
| 07 Espina Jade | 0,735 | **0,294** | 0,976 | Sí, en `pixel` |
| 08 Brasa Celeste | 0,642 | 0,493 | 1,059 | No |
| 09 Llama Dorada | 0,686 | 0,370 | 1,023 | No |
| 10 Bruma Gris | 0,642 | 0,395 | 0,951 | No |

### Interpretación

- **Ningún personaje es copia de una imagen de entrenamiento.** En `cnn` y
  `forma` los diez quedan muy por encima del umbral, y en las figuras ninguna
  silueta coincide con la de su vecina.
- **Dos alertas en `pixel` (04 y 07).** Su vecina más cercana es la misma
  imagen: una cabeza de dragón marrón sobre fondo gris pardo liso. Lo que
  coincide es el fondo y la paleta, no la figura: en `forma` ambos quedan
  cerca de la mediana entre reales (0,981).
- **Los vecinos comparten color y fondo.** Rojo sobre celeste para 05, 08 y 09;
  gris para 10; ocre para 02. El generador aprendió las combinaciones de color
  del dataset.
- **Estar lejos no es solo buena noticia.** En `cnn` los personajes están a
  0,60–0,74 de su vecina, el doble de la mediana entre reales (0,302). No son
  copias, pero tampoco se parecen a un dragón real del dataset: son siluetas
  más abstractas, con menos detalle.

### El personaje más difícil de defender

**04, Ámbar Errante.** Es el que queda más cerca de una imagen real en píxeles
(0,281, bajo el percentil 5). Su figura naranja no reproduce la cabeza de la
vecina, pero el fondo pardo y los tonos naranjas sí son casi los mismos.

Este caso muestra qué aprendió la GAN: primero lo más fácil y repetido del
dataset —fondos lisos, paletas y trazos de escamas—, y solo parcialmente la
estructura de un dragón. La novedad de nuestros personajes viene de formas que
no existen en el dataset, pero su color y su fondo sí están tomados de él.
