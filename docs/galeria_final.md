# Galería final y registro de selección

**Estado: pendiente.** Todavía no hay candidatos del entrenamiento final, así
que no se ha seleccionado ningún personaje. Este documento describe el
procedimiento ya probado y se completa con los resultados reales.

## Procedimiento

1. Crear la tabla de evaluación a partir de los candidatos:

   ```powershell
   .\.venv\Scripts\python.exe scripts/evaluation_table.py --candidates runs/candidates_v3
   ```

2. Llenar las notas en `docs/data/evaluacion_candidatos.csv` según
   `docs/criterios_evaluacion.md` y calcular las decisiones:

   ```powershell
   .\.venv\Scripts\python.exe scripts/evaluation_table.py --decide docs/data/evaluacion_candidatos.csv
   ```

3. Escribir los diez elegidos en `docs/data/seleccion_final.csv`, con las
   columnas `file` y `motivo`.

4. Armar la galería:

   ```powershell
   .\.venv\Scripts\python.exe scripts/build_gallery.py --candidates runs/candidates_v3
   ```

5. Buscar los vecinos más cercanos de los diez (`docs/vecinos_cercanos.md`).

## Contenido de `galeria/`

| Archivo | Contenido |
|---|---|
| `personaje_01.png` … `personaje_10.png` | Los diez PNG, copia exacta del candidato |
| `registro_seleccion.csv` | Identificador, candidato de origen, semilla y motivo |
| `galeria_selection.json` | Semilla y vector z de cada uno, y huella del checkpoint |

`galeria_selection.json` es el manifiesto que entrega el generador de la parte 1,
reducido a los diez elegidos. Permite regenerarlos:

```powershell
.\.venv\Scripts\python.exe -m dragon_gan.generate --checkpoint runs/final_v3/<variante>/last.pt --output runs/galeria_regenerada --manifest galeria/galeria_selection.json
```

## Tasa de selección

Tasa = 10 ÷ total de candidatos generados × 100.

`build_gallery.py` la calcula con el total del manifiesto. Si se generaron
varias tandas, el total real se indica con `--total`.

| Dato | Valor |
|---|---|
| Candidatos generados | pendiente |
| Personajes seleccionados | pendiente |
| Tasa de selección | pendiente |

## Prueba del procedimiento

Se probó de punta a punta con un modelo de 4 épocas y 30 candidatos, solo para
verificar el código (sus imágenes no son resultados del proyecto): la galería
de 10 se regeneró con `dragon_gan.generate` y los 10 PNG coincidieron byte a
byte con los seleccionados.
