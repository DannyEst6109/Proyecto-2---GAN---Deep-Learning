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

Pendiente: se completa cuando exista la galería final.
