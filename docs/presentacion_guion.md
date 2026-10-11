# Guion de la presentación

Fuente de `presentacion.pptx`: cada sección `##` es una diapositiva, cada viñeta
es una línea de texto y la imagen (si existe el archivo) va a la derecha.
Generar con `python scripts/build_presentation.py`. Máximo 12 diapositivas;
lo que va después de la 12 son anexos. Las líneas con PENDIENTE se reemplazan
con resultados reales del entrenamiento final.

## 1. Dragones de fantasía medieval generados con una GAN

- Proyecto 2 · Deep Learning 2026 · Universidad del Valle de Guatemala
- Daniel Estrada y Daniela Ramírez de León
- Universo: dragones de fantasía medieval, con escamas, cuernos y alas
- Estilo: ilustración, colores terrosos y oscuros, cielos y fondos simples
- Referencia visual: Game of Thrones. Los personajes deben ser nuevos
- Vara para juzgar la galería: que se reconozca un dragón, con cabeza y cuerpo o alas, y que no repita a otro

## 2. Datos: origen, permiso y preparación

- Dino or Dragon? de agrigorev (Kaggle, versión 1). Licencia CC0
- Imágenes sintéticas de Stable Diffusion v1.4; no son fotogramas de la serie
- 965 dragones revisados: 0 archivos dañados y 0 duplicados
- 9 descartadas: 5 cartas con texto, 1 negra, 2 recortes extremos, 1 foto de un dibujo
- Versión final: 956 imágenes, misma para los tres experimentos
- Preparación: RGB, 512×512 a 64×64 con Lanczos, normalización a [-1, 1]
- Aumento: volteo horizontal aleatorio (p = 0,5)

![Muestra después del cargador](img/muestra_cargador.png)

## 3. Arquitectura: DCGAN de 64×64

- Elegida por ser la base más simple y estable para pocos datos y 64×64
- Generador: z de 100 → 4 convoluciones transpuestas con BatchNorm y ReLU → Tanh
- Canales del generador: 512, 256, 128, 64, 3 (3,6 millones de parámetros)
- Discriminador: 4 convoluciones con BatchNorm y LeakyReLU(0,2) → 1 logit (2,8 millones)
- Adam, lr 0,0002, betas (0,5; 0,999), lote 64, 600 épocas, semilla 42
- El código regenera la galería desde las semillas y vectores z guardados

## 4. Experimentos: hipótesis previas y control

- Un solo cambio por variante; mismos datos, semilla, épocas, z y ruido fijo
- Pérdida: no saturante (base) frente a minimax original
- Hipótesis: creemos que la no saturante mejorará el aprendizaje porque minimax da gradientes casi nulos cuando D rechaza con confianza. Útil si aparecen dragones antes o mejores, sin perder diversidad
- Estabilización: normalización espectral en D frente a BatchNorm
- Hipótesis: creemos que mejorará estabilidad y diversidad porque limita a D. Útil si D(real) y D(fake) se alejan de 1 y 0 y el ruido fijo conserva diversidad
- Hipótesis escritas antes de entrenar: docs/hypotheses/v3/

## 5. Resultados de los experimentos

- PENDIENTE: tabla con D(real), D(fake), pérdida D y diversidad por variante
- PENDIENTE: ¿se cumplió la hipótesis de pérdida? Evidencia
- PENDIENTE: ¿se cumplió la hipótesis de estabilización? Evidencia
- PENDIENTE: modelo y época elegidos, y por qué

## 6. Evidencia 1: rejilla de ruido fijo

- Los mismos 16 vectores z en varias épocas
- PENDIENTE: en qué época aparecen formas reconocibles
- PENDIENTE: posiciones que empiezan a parecerse entre sí

## 7. Evidencia 2: curvas de pérdida interpretadas

- En una GAN sana las curvas no bajan juntas: se estabilizan enfrentadas
- PENDIENTE: qué muestran las curvas de G y D de cada variante
- PENDIENTE: épocas con D cercano a cero o picos de G

## 8. Problemas encontrados y decisiones

- Primera selección: solo cuerpo completo, 22 imágenes
- Resultado: colapso de modos. Las 16 muestras eran casi iguales y D(fake) ≈ 0,01
- 0 de 600 candidatos aceptados. Se conserva como evidencia del fallo
- Decisión: usar todos los dragones, agregar volteo y subir a 64 canales base
- Decisión: cambiar la estabilización de ruido en D a normalización espectral
- PENDIENTE: problemas observados en el entrenamiento final

## 9. Galería: diez personajes

- PENDIENTE: los diez PNG con nombre y clase
- PENDIENTE: tasa de selección = 10 ÷ candidatos generados × 100
- Criterio: seis notas de 0 a 2 definidas antes de ver los candidatos
- Se acepta con dragón = 2, ningún criterio en 0 y suma de 9 o más

## 10. Evidencia 3: vecinos más cercanos

- Cada personaje junto a sus 5 imágenes de entrenamiento más parecidas
- Métrica principal: características de ResNet-18 preentrenada
- Comprobaciones: píxeles y forma en grises; también contra imágenes volteadas
- Referencia: distancia entre imágenes reales. Alerta si queda bajo el percentil 5
- Prueba del método: detecta una copia exacta y una volteada con distancia 0
- PENDIENTE: figura y distancias de los diez personajes

## 11. Reflexión, conclusiones y limitaciones

- PENDIENTE: el personaje más difícil de defender como nuevo y qué dice de lo que aprendió la GAN
- PENDIENTE: conclusiones de los dos experimentos
- Limitación: datos sintéticos que heredan errores de anatomía de Stable Diffusion
- Limitación: 956 imágenes de estilos mezclados y resolución de 64×64
- Limitación: una sola semilla; la evaluación visual es subjetiva
- Los vecinos aportan evidencia de semejanza, no prueban novedad

## 12. Matriz de evidencias

- Universo y datos · diap. 1 y 2 · origen CC0 documentado · datos sintéticos
- GAN y regeneración · diap. 3 · PENDIENTE · PENDIENTE
- Experimento de pérdida · diap. 4 y 5 · PENDIENTE · una semilla
- Experimento de estabilización · diap. 4 y 5 · PENDIENTE · una semilla
- Ruido fijo · diap. 6 · PENDIENTE · 16 vectores
- Curvas de pérdida · diap. 7 · PENDIENTE · no miden calidad
- Galería y tasa de selección · diap. 9 · PENDIENTE · selección subjetiva
- Vecinos más cercanos · diap. 10 · PENDIENTE · no prueban novedad
- Fallos y colapso · diap. 8 · colapso con 22 imágenes · causa no aislada

## Anexo A. Criterios de evaluación de candidatos

- dragon: ¿se reconoce como dragón?
- cuerpo_alas: ¿se ven cuerpo y alas?
- universo: ¿encaja en fantasía medieval?
- anatomia: ¿tiene deformaciones?
- distinto: ¿se diferencia de otros candidatos?
- novedad: ¿se diferencia del entrenamiento?

## Anexo B. Uso de asistentes de IA

- Se usaron asistentes de IA para programar, revisar el dataset y documentar
- Detalle en README.md
- Ninguna imagen de la galería proviene de un generador externo
