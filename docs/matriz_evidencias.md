# Matriz de evidencias

Columnas que pide el enunciado: evidencia, diapositiva, conclusión y
limitación. Se agrega la ubicación real del archivo y quién lo produce.

Estado al 11 de octubre de 2026: las filas marcadas como **pendiente** dependen
del entrenamiento final (v3), que todavía no tiene resultados en el repositorio.

| Requisito | Evidencia y ubicación | Diap. | Conclusión | Limitación | Responsable |
|---|---|---:|---|---|---|
| Universo definido | `README.md`, `docs/presentacion_guion.md` | 1 | Dragones de fantasía medieval con escamas, cuernos y alas | La referencia a Game of Thrones es solo visual | Ambos |
| Procedencia del dataset | `docs/ficha_dataset.md` | 2 | Dino or Dragon?, Kaggle, CC0, ZIP verificado por SHA-256 | Imágenes sintéticas de Stable Diffusion | Persona 2 |
| Selección y preparación | `docs/data/curation_final_v4.csv`, `docs/data/exclusiones_persona2.csv`, `docs/preparacion_dataset.md`, `docs/img/muestra_cargador.png` | 2 | 956 de 965 aceptadas; 64×64, [-1, 1], volteo horizontal | Revisión visual subjetiva sobre miniaturas | Persona 2 |
| GAN entrenada por el equipo | `dragon_gan/`, `configs/final_v3.json`, pesos: **pendiente** | 3 | **Pendiente** | **Pendiente** | Persona 1 |
| Experimento de pérdida | `docs/hypotheses/v3/loss.txt`, resultados: **pendiente** | 4, 5 | **Pendiente** | Una sola semilla | Persona 1 |
| Experimento de estabilización | `docs/hypotheses/v3/stabilization.txt`, resultados: **pendiente** | 4, 5 | **Pendiente** | Una sola semilla | Persona 1 |
| Evolución con ruido fijo | Rejillas por época: **pendiente** | 6 | **Pendiente** | Solo 16 vectores z | Persona 1 |
| Curvas de pérdida interpretadas | Gráficas y análisis: **pendiente** | 7 | **Pendiente** | Las pérdidas no miden calidad | Persona 1 |
| Fallos y colapso de modos | `docs/resultados_fullbody_v2.md`, `docs/data/fullbody_result_v2.json` | 8 | Con 22 imágenes las tres variantes colapsaron: 0 de 600 aceptados | No se aisló una causa única | Persona 1 |
| Criterios de evaluación | `docs/criterios_evaluacion.md`, `scripts/evaluation_table.py` | 9, anexo A | Seis criterios de 0 a 2 definidos antes de ver candidatos | Evaluación visual, sin FID | Persona 2 |
| Evaluación de candidatos | `docs/data/evaluacion_candidatos.csv`: **pendiente** | 9 | **Pendiente** | **Pendiente** | Persona 2 |
| Diez personajes distintos | `galeria/`: **pendiente** | 9 | **Pendiente** | **Pendiente** | Ambos |
| Tasa de selección | `galeria/registro_seleccion.csv`: **pendiente** | 9 | **Pendiente** | Selección subjetiva | Persona 2, con el conteo de persona 1 |
| Vecinos más cercanos: método | `scripts/nearest_neighbors.py`, `docs/vecinos_cercanos.md` | 10 | Detecta copias exactas y volteadas con distancia 0 en las tres métricas | No demuestra novedad por sí solo | Persona 2 |
| Vecinos más cercanos: resultados | `docs/vecinos/`: **pendiente** | 10 | **Pendiente** | **Pendiente** | Persona 2 |
| Reproducibilidad | `galeria/galeria_selection.json`: **pendiente**; `dragon_gan/generate.py` | 3, 9 | Procedimiento probado: 10 de 10 PNG regenerados idénticos con un modelo de prueba | Igualdad exacta solo en el mismo entorno | Persona 1 |
| Reflexión y limitaciones | `docs/presentacion_guion.md`: **pendiente** | 11 | **Pendiente** | **Pendiente** | Ambos |
| Uso de IA | `README.md` | anexo B | Declarado | — | Ambos |
