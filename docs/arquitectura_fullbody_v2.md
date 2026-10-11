# Arquitectura y objetivos de entrenamiento

La ejecución `fullbody_v2` usa DCGAN RGB de 64×64. El código es
`dragon_gan/models.py`; sus dimensiones se derivan de la configuración congelada.

## Generador: 1 100 224 parámetros

Entrada: z normal estándar con forma (N, 100, 1, 1).

| Operación | Canales de salida | Resolución | Activación |
|---|---:|---:|---|
| ConvTranspose2d, kernel 4, stride 1, padding 0 | 256 | 4×4 | BatchNorm + ReLU |
| ConvTranspose2d, kernel 4, stride 2, padding 1 | 128 | 8×8 | BatchNorm + ReLU |
| ConvTranspose2d, kernel 4, stride 2, padding 1 | 64 | 16×16 | BatchNorm + ReLU |
| ConvTranspose2d, kernel 4, stride 2, padding 1 | 32 | 32×32 | BatchNorm + ReLU |
| ConvTranspose2d, kernel 4, stride 2, padding 1 | 3 | 64×64 | Tanh |

## Discriminador: 694 656 parámetros

Entrada: imágenes RGB normalizadas a [-1, 1].

| Operación | Canales de salida | Resolución | Activación |
|---|---:|---:|---|
| Conv2d, kernel 4, stride 2, padding 1 | 32 | 32×32 | LeakyReLU(0.2) |
| Conv2d, kernel 4, stride 2, padding 1 | 64 | 16×16 | BatchNorm + LeakyReLU(0.2) |
| Conv2d, kernel 4, stride 2, padding 1 | 128 | 8×8 | BatchNorm + LeakyReLU(0.2) |
| Conv2d, kernel 4, stride 2, padding 1 | 256 | 4×4 | BatchNorm + LeakyReLU(0.2) |
| Conv2d, kernel 4, stride 1, padding 0 | 1 | 1×1 | Logit sin sigmoid |

No se usan sesgos en las convoluciones. Inicialización normal de pesos de
convolución (media 0, desviación 0.02); BatchNorm con pesos normales (media 1,
desviación 0.02) y sesgos cero. Las puntuaciones registradas aplican sigmoid al
logit; las pérdidas se calculan con softplus para evitar logaritmos inestables.

## Pérdidas implementadas

Si a es el logit de D y softplus(a)=log(1+exp(a)):

- D: media de softplus(−a_real) y softplus(a_fake), dividida entre dos.
- G base y estabilización: media de softplus(−a_fake), objetivo no saturante.
- G variante de pérdida: media de −softplus(a_fake), objetivo minimax original.

Ambos optimizadores minimizan sus respectivos objetivos. La pérdida minimax
puede ser negativa y no se compara numéricamente con la pérdida no saturante
como una medida común de calidad. En estabilización se añade ruido gaussiano
independiente con desviación 0.05 a las entradas de D, también durante el paso
de G; no se recorta el ruido a [-1, 1] y no se aplica al generar candidatos.

Una actualización de D va seguida de una de G por lote. Las imágenes falsas se
desconectan del grafo durante el paso de D; durante el paso de G se desactivan los
gradientes de los parámetros de D, manteniendo gradiente hacia G. D conserva
su modo de entrenamiento y las estadísticas de BatchNorm se actualizan en
ambos pasos. Este comportamiento se mantiene en las tres variantes.

## Preparación y reproducibilidad

Los originales se cargan con orientación EXIF corregida, RGB, relleno proporcional
si procede, reducción a 64×64 y normalización. Las imágenes seleccionadas del ZIP
son cuadradas, por lo que no requieren relleno por proporción. No hay aumentos.
Se usan generadores aleatorios separados para orden de datos, ruido de entrada
y ruido fijo, conservando los estados en checkpoints. El ruido z de entrenamiento
utiliza la secuencia de PyTorch controlada por semilla 42.

La galería utiliza el modo evaluación de G y los vectores guardados. La resolución
64×64 y el conjunto pequeño limitan detalle anatómico, diversidad y generalización;
la arquitectura por sí sola no garantiza personajes completos ni nuevos.
