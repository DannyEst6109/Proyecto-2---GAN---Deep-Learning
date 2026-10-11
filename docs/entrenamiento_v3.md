# Parte 1, versión 3: 965 dragones en GPU

## Por qué una v3

En v2 (22 imágenes, 300 épocas = 900 actualizaciones) las tres variantes colapsaron:
las 16 muestras de ruido fijo eran prácticamente iguales (desviación entre muestras
≈ 0,013 en la escala [-1, 1]) y D separaba reales y falsas con D(real) ≈ 0,98 y
D(fake) ≈ 0,01 desde la época ~30. D memorizó el conjunto y G solo aprendió texturas.
Se descartó que fuera un efecto de generar en modo `eval()`: en modo `train()` el
resultado es el mismo. Esta ejecución se conserva como evidencia de colapso de modos.

Una prueba de 40 épocas (≈480 actualizaciones) con las 767 imágenes de entrenamiento
ya no colapsó: las muestras variaban entre sí, aunque todavía eran texturas.
Conclusión: el problema principal eran los datos y el presupuesto, no el código.

## Cambios respecto de v2 (decididos antes de entrenar v3)

| Aspecto | v2 | v3 |
|---|---|---|
| Datos | 22 seleccionadas a mano (cuerpo completo) | 965: todos los dragones del ZIP (train 767 + test 198) |
| Aumento | ninguno | volteo horizontal aleatorio (p = 0,5) |
| Red | 32 canales base | 64 canales base (DCGAN estándar) |
| Lote / épocas | 8 / 300 (900 pasos) | 64 / 600 (≈9 600 pasos) |
| lr G / lr D | 2e-4 / 1e-4 | 2e-4 / 2e-4 |
| Experimento de pérdida | minimax frente a no saturante | igual |
| Estabilización | ruido gaussiano 0,05 en D | normalización espectral en D |
| Dispositivo | CPU | GPU de Colab (CPU: ~30 s por época, inviable) |

Ya no se filtra por encuadre de cuerpo completo: el universo admite retratos y
cuerpos completos de dragones. Selección: `docs/data/curation_all_v3.csv`
(ruta, SHA-256 y decisión de cada imagen). Configuración: `configs/final_v3.json`.
Hipótesis escritas antes de entrenar: `docs/hypotheses/v3/`.

La normalización espectral (Miyato et al., 2018) se aplica a todas las
convoluciones de D y sustituye su BatchNorm, como en SN-GAN. Es el único cambio de
la variante `stabilization` (`stabilization_change` en la configuración).
`isolate_init_rng` inicializa G antes de construir D y reinicia la semilla después,
para que las tres variantes tengan el mismo G inicial y la misma secuencia de z
aunque D sea diferente. `smoke_test` lo comprueba.

Otros cambios técnicos: el dataset guarda en memoria cada imagen ya reducida, en
lugar de decodificar los JPG en cada época; `snapshot_every` guarda G cada 50 épocas
para poder elegir una época intermedia; `checkpoint_every` guarda el checkpoint
completo cada 10 épocas y en la última.

## Ejecución

Abrir `output/jupyter-notebook/parte_1_gan.ipynb` en Google Colab con GPU T4
(*Archivo → Abrir cuaderno → GitHub*, o subir el archivo). El notebook clona el
repositorio, descarga el ZIP de Kaggle, prepara los datos, entrena las tres variantes,
genera el informe, la diversidad por snapshot, 200 candidatos, la galería regenerable
y un ZIP para persona 2. Todo se guarda en `MyDrive/proyecto2_gan`. Si la sesión se
corta, se vuelve a ejecutar desde arriba y se reanuda.

Equivalente por línea de comandos:

```bash
python scripts/prepare_dataset.py --selection docs/data/curation_all_v3.csv --output data/dragons_all_v3
python -m scripts.run_experiments --config configs/final_v3.json --data data/dragons_all_v3 --output runs/final_v3 --device cuda --purpose project --hypotheses docs/hypotheses/v3
python -m scripts.compare_experiments --runs runs/final_v3 --output runs/final_v3/report
python -m dragon_gan.generate --checkpoint runs/final_v3/<variante>/last.pt --output runs/candidates_v3 --count 200 --seed 1000
```

## Para persona 2

- Vecinos más cercanos: buscar en `data/dragons_all_v3` (las 965 imágenes de entrenamiento).
- Tasa de selección: 10 de 200 candidatos (semillas 1000–1199), más el criterio.
- La galería se regenera con `dragon_gan.generate --manifest galeria_selection.json`.
