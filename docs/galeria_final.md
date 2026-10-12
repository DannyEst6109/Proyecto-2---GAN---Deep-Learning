# Galería final y registro de selección

Modelo: base (pérdida no saturante), época 450. Pesos: `pesos/generator_epoch_0450.pt`.

![Galería](img/galeria_mosaico.png)

| Id | Nombre | Clase | Candidato | Semilla | Motivo |
|---|---|---|---|---:|---|
| `personaje_01.png` | Ceniza Alta | Centinela de las torres | `dragon_0002` | 1001 | Figura erguida con cuello largo y alas |
| `personaje_02.png` | Musgo Viejo | Guardián del pantano | `dragon_0014` | 1013 | Único verde azulado sobre fondo ocre |
| `personaje_03.png` | Garra Sombría | Acechador nocturno | `dragon_0025` | 1024 | Silueta oscura serpentina con garras |
| `personaje_04.png` | Ámbar Errante | Mensajero de las dunas | `dragon_0033` | 1032 | Cuerpo serpentino naranja con cabeza y garra |
| `personaje_05.png` | Fauce Carmesí | Heraldo de guerra | `dragon_0053` | 1052 | La cabeza de perfil más clara |
| `personaje_06.png` | Vela Nocturna | Exploradora de tormentas | `dragon_0055` | 1054 | Figura violeta con alas y patas |
| `personaje_07.png` | Espina Jade | Custodio del bosque | `dragon_0064` | 1063 | Única paleta verde y dorada |
| `personaje_08.png` | Brasa Celeste | Campeón de los cielos | `dragon_0152` | 1151 | Dragón rojo sobre azul |
| `personaje_09.png` | Llama Dorada | Portadora del fuego | `dragon_0164` | 1163 | Criatura naranja y amarilla en vuelo |
| `personaje_10.png` | Bruma Gris | Espectro de las cumbres | `dragon_0169` | 1168 | Único monocromo gris con alas |

Los nombres y clases los puso el equipo; el modelo solo genera la imagen.

## Tasa de selección

| Dato | Valor |
|---|---|
| Candidatos generados | 200 (semillas 1000–1199) |
| Personajes seleccionados | 10 |
| Tasa de selección | 10 ÷ 200 × 100 = **5 %** |

Criterio: `docs/criterios_evaluacion.md`. Resultado de la evaluación:
`docs/evaluacion_candidatos.md`. Ningún candidato alcanzó la categoría
"aceptar"; los diez salen de los doce en "reserva".

## Contenido de `galeria/`

| Archivo | Contenido |
|---|---|
| `personaje_01.png` … `personaje_10.png` | Los diez PNG, copia exacta del candidato |
| `registro_seleccion.csv` | Identificador, candidato de origen, semilla, nombre, clase y motivo |
| `galeria_selection.json` | Semilla y vector z de cada uno, y huella del checkpoint |

## Regenerar la galería

```powershell
.\.venv\Scripts\python.exe -m dragon_gan.generate --checkpoint pesos/generator_epoch_0450.pt --output runs/galeria_regenerada --manifest galeria/galeria_selection.json
```

El comando comprueba que el checkpoint sea el declarado (SHA-256) y genera los
diez PNG desde sus vectores z.

Comprobación del 11 de octubre de 2026 en CPU local (PyTorch 2.14.1): los diez
se regeneran con una diferencia máxima de 1 nivel sobre 255 por píxel respecto
a los originales generados en Colab (PyTorch 2.11.0). No son idénticos byte a
byte porque cambia la versión de PyTorch y el hardware.

## Procedimiento seguido

`<candidatos>` es la carpeta `candidates_base_450` del ZIP de la parte 1.

```powershell
.\.venv\Scripts\python.exe scripts/evaluation_table.py --candidates <candidatos>
.\.venv\Scripts\python.exe scripts/evaluation_table.py --decide docs/data/evaluacion_candidatos.csv
.\.venv\Scripts\python.exe scripts/build_gallery.py --candidates <candidatos>
.\.venv\Scripts\python.exe -m scripts.nearest_neighbors --generated galeria --metric cnn
```

Las notas se llenan a mano en `docs/data/evaluacion_candidatos.csv` y los diez
elegidos se escriben en `docs/data/seleccion_final.csv` (`file`, `motivo`,
`nombre`, `clase`).
