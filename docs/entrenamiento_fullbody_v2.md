# Ejecuciones con cuerpo completo: versión 2

Se mantiene la decisión del usuario de entrenar con cuerpo completo y ampliar la
selección. Se revisaron de nuevo las 767 imágenes de entrenamiento del ZIP original
y se ampliaron los estilos admitidos a ilustraciones en color y monocromas.
Tras revisar 47 candidatas ampliadas se conservaron 22; se excluyeron retratos,
recortes importantes, ejemplos con varios personajes/cabezas y casos dudosos.
La selección es asistida y subjetiva; requiere revisión del equipo.

El registro completo está en `docs/data/curation_fullbody_v2.csv`, con ruta, decisión
y SHA-256. Los originales están en `data/dragons_fullbody_v2`, sin modificar.
El manifiesto y procedencia están en `docs/data/fullbody_manifest_v2.json`.
Las 198 imágenes de prueba siguen reservadas en el ZIP; no se utilizaron para entrenar.
Los seis ejemplos del piloto se conservan en su carpeta anterior.

Origen: Dino or Dragon?, agrigorev, versión 1. Licencia publicada: CC0. Imágenes
sintéticas de Stable Diffusion v1.4. No son fotogramas de Game of Thrones.
Un conjunto de 22 imágenes es pequeño para aprender variedad de personajes;
no se presupone que permita obtener diez resultados defendibles como nuevos.

## Presupuesto congelado antes de las comparaciones

Configuración: `configs/fullbody_v2.json`. DCGAN RGB de 64×64, vector z de 100,
32 canales base, batch_size 8, 300 épocas, cuatro hilos en CPU, semilla 42.
Adam con betas (0.5, 0.999), lr G=0.0002 y lr D=0.0001. La red tiene menos canales
que la propuesta inicial para reducir coste local; la tasa de D se fijó menor que
la de G antes de comparar, dado el rápido dominio de D en el ensayo anterior.
Son decisiones de diseño, no valores demostrados óptimos ni experimentos adicionales.
Cada época usa tres lotes, con el último incompleto de seis imágenes: 900 actualizaciones
por modelo y variante. No hay aumentos aleatorios de datos.

Un benchmark previo de dos épocas sobre esta selección completó el entrenamiento
con tiempos del bucle de aproximadamente 0.8 y 0.7 segundos. La estimación no
incluye inicialización, gráficos y checkpoints. El benchmark se conserva en
`runs/fullbody_v2_benchmark` y no se utiliza como inicio de las comparaciones.

Las tres ejecuciones parten de nuevo, con hipótesis de `docs/hypotheses/`, plan y
hashes de código guardados antes de entrenar. Solo cambia la pérdida de G en
`loss`, o el ruido 0.05 de entrada en D en `stabilization`. Los datos, presupuesto,
inicialización, secuencia de z y ruido fijo se mantienen controlados.

## Reproducción

```powershell
.\.venv\Scripts\python.exe scripts/prepare_dataset.py --selection docs/data/curation_fullbody_v2.csv --output data/dragons_fullbody_v2
.\.venv\Scripts\python.exe -m scripts.run_experiments --config configs/fullbody_v2.json --data data/dragons_fullbody_v2 --output runs/fullbody_v2 --device cpu --purpose project
.\.venv\Scripts\python.exe -m scripts.compare_experiments --runs runs/fullbody_v2 --output runs/fullbody_v2/report
```

Para reanudar añadir `--resume` al comando de ejecución. Conservar versiones del
entorno, configuración, datos e hipótesis. Los resultados están excluidos de Git;
los metadatos y comandos permiten reconstruir el procedimiento.
