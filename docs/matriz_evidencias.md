# Matriz de evidencias

Columnas que pide el enunciado: evidencia, diapositiva, conclusión y
limitación. Se agrega la ubicación real del archivo y quién lo produjo.
La versión de una diapositiva está en la diapositiva 12 de `presentacion.pdf`.

| Requisito | Evidencia y ubicación | Diap. | Conclusión | Limitación | Responsable |
|---|---|---:|---|---|---|
| Universo definido | `README.md` | 1 | Dragones de fantasía medieval con escamas, cuernos y alas | Game of Thrones es solo referencia visual | Ambos |
| Procedencia del dataset | `docs/ficha_dataset.md` | 2 | Dino or Dragon?, Kaggle, CC0, ZIP verificado por SHA-256 | Imágenes sintéticas de Stable Diffusion | Persona 2 |
| Selección y preparación | `docs/data/curation_final_v4.csv`, `docs/data/exclusiones_persona2.csv`, `docs/preparacion_dataset.md` | 2 | 956 de 965 aceptadas; 64×64, [-1, 1], volteo horizontal | Revisión visual subjetiva sobre miniaturas | Persona 2 |
| GAN entrenada por el equipo | `dragon_gan/`, `configs/final_v4.json`, `pesos/generator_epoch_0450.pt` | 3 | DCGAN 64×64 entrenada 600 épocas en GPU T4 | Siluetas abstractas, sin anatomía completa | Persona 1 |
| Experimento de pérdida | `docs/hypotheses/v3/loss.txt`, `docs/resultados_v3.md` | 4, 5 | Hipótesis confirmada: minimax satura y G no aprende | Una sola semilla | Persona 1 |
| Experimento de estabilización | `docs/hypotheses/v3/stabilization.txt`, `docs/resultados_v3.md` | 4, 5 | Hipótesis rechazada: la normalización espectral colapsó | No se probó otra tasa de aprendizaje para D | Persona 1 |
| Evolución con ruido fijo | `docs/img/v3_evolucion_base.png`, `docs/img/v3_ruido_fijo_variantes.png` | 5, 6 | Siluetas desde la época 150; sin colapso en la base | Solo 16 vectores z | Persona 1 |
| Curvas de pérdida interpretadas | `docs/img/v3_curvas.png`, `docs/resultados_v3.md` | 7 | D domina 268 épocas en la base; curvas planas no implican calidad | Las pérdidas no miden calidad | Persona 1 |
| Fallos y colapso de modos | `docs/resultados_fullbody_v2.md`, `docs/resultados_v3.md` | 5, 8 | Colapso con 22 imágenes y con normalización espectral | No se aisló una causa única | Persona 1 |
| Criterios de evaluación | `docs/criterios_evaluacion.md` | 9, anexo A | Seis criterios de 0 a 2 definidos antes de ver candidatos | Evaluación visual, sin FID | Persona 2 |
| Evaluación de candidatos | `docs/data/evaluacion_candidatos.csv`, `docs/data/prefiltro_candidatos.csv`, `docs/evaluacion_candidatos.md` | 9 | De 2 000: 4 aceptados, 32 en reserva, 365 descartados y 1 599 fuera del prefiltro | Los descartados se calificaron en grupo | Persona 2 |
| Diez personajes distintos | `galeria/`, `docs/galeria_final.md` | 9 | Diez personajes de poses y paletas distintas: 4 dragones claros y 6 siluetas | Anatomía incompleta en la mayoría | Ambos |
| Tasa de selección | `galeria/registro_seleccion.csv` | 9 | 10 de 2 000 = 0,5 % | Selección subjetiva | Persona 2, con el conteo de persona 1 |
| Vecinos más cercanos | `scripts/nearest_neighbors.py`, `docs/vecinos/`, `docs/vecinos_cercanos.md` | 10, anexo B | Ninguna copia ni alerta; los vecinos comparten paleta y fondo | No demuestra novedad por sí solo | Persona 2 |
| Reproducibilidad | `galeria/galeria_selection.json`, `dragon_gan/generate.py`, `pesos/` | 3 | Los diez se regeneran idénticos byte a byte | Igualdad byte a byte solo en el mismo entorno | Persona 1 |
| Reflexión final | `docs/vecinos_cercanos.md` | 11 | Marea Azul (07) es el más difícil de defender: comparte paleta, fondo y composición con su vecina | Análisis visual | Ambos |
| Uso de IA | `README.md` | anexo D | Declarado | — | Ambos |
