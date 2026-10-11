# Trabajo local y colaboración por GitHub

Repositorio: https://github.com/DannyEst6109/Proyecto-2---GAN---Deep-Learning

GitHub sincroniza código y documentación. No ejecuta el entrenamiento de las
computadoras ni sincroniza automáticamente los datos, pesos o entornos virtuales.
Cada integrante instala su entorno y conserva su copia del dataset acordado.

## Preparación en Windows (PowerShell)

Se verificará inicialmente con Python 3.13.7. Desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/check_environment.py
.\.venv\Scripts\python.exe -m jupyterlab
```

No es necesario activar el entorno ni cambiar la política de ejecución de PowerShell.
El archivo de dependencias base usa PyTorch para CPU, adecuado para este equipo.
Si el compañero tiene NVIDIA compatible, debe instalar una compilación CUDA de
las mismas versiones de torch/torchvision según el selector oficial de PyTorch:
https://pytorch.org/get-started/locally/
No ejecutar después la instalación CPU sobre ese entorno CUDA.
El comprobador elige CUDA cuando está disponible y CPU en caso contrario.
Otras GPU necesitan revisar su backend por separado; no se habilitan automáticamente.

## Incorporación del compañero

El propietario del repositorio debe dar acceso de escritura al compañero.
Después de aceptar la invitación:

```powershell
git clone https://github.com/DannyEst6109/Proyecto-2---GAN---Deep-Learning.git
cd Proyecto-2---GAN---Deep-Learning
```

Instalar el entorno siguiendo los pasos anteriores. No copiar `.venv` entre equipos.

## Organización de cambios

Acuerdo del equipo: trabajar siempre en `main`, sin crear nuevas ramas.
Codex no debe hacer commits ni subir cambios; esas operaciones las realizará el usuario.

- Parte 1: `dragon_gan/` y notebook de entrenamiento.
- Persona 2: datos, evaluación y presentación; conservar su notebook por separado.
- Coordinar modificaciones de README, configuración y documentación compartida.
- Antes de actualizar desde GitHub, revisar `git status` y proteger el trabajo local.
- Evitar editar simultáneamente el mismo archivo o notebook.

## Datos y resultados

`data/`, `runs/`, `.venv/` y pesos `.pt`/`.pth` están excluidos por `.gitignore`.
Compartirlos por una ubicación acordada, documentar el enlace y comprobar el hash
del dataset. Incluir la galería final en su carpeta de entrega; no confundirla con
las muestras temporales de `runs/`.

## Presupuesto de entrenamiento

Todavía no se ha medido rendimiento de la GAN. CPU permite desarrollar y verificar
el código, pero el entrenamiento completo puede ser lento. Medir una ejecución
corta antes de fijar épocas, batch y presupuesto de las tres comparaciones.
Registrar versiones y hardware en cada ejecución; comparar preferentemente en
el mismo equipo para reducir diferencias entre entornos.
