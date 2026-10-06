# Entrega de datos de persona 2 a persona 1

Antes de entrenar, entregar:

1. Imágenes legibles organizadas en una carpeta, con estilo consistente.
   Encuadre elegido: dragones de cuerpo completo, con alas y anatomía visibles;
   evitar recortes que eliminen estas partes al preparar las imágenes.
2. Documento con origen, URL, licencia o permiso de uso y cantidad de imágenes.
   Una referencia visual a una serie no demuestra permiso para utilizar sus imágenes.
3. Procedimiento o código de limpieza y preparación: duplicados, recorte,
   resolución, canales, normalización y aumentos, si se usan.
4. Un manifiesto con identificador, ruta, fuente y SHA-256 de cada imagen.
   La evaluación de vecinos debe poder identificar la imagen original.
5. Una muestra visual del dataset para revisar juntos antes de cerrar la versión.

Propuesta de entrada al modelo: RGB, 64×64 y normalización a [-1, 1].
Persona 1 y persona 2 deben acordar dónde se aplican las transformaciones para
no recortar o normalizar dos veces las mismas imágenes.

Cerrar una versión del dataset y conservarla en todas las comparaciones.
No mezclar cambios de datos con cambios de pérdida o estabilización.
Registrar el hash del manifiesto en la configuración de cada ejecución.

Modalidad acordada: entorno local. Comprobar el hardware de cada computadora
y conservar checkpoints, registros y ruido fijo en almacenamiento persistente.
Los datos y pesos se comparten mediante una ubicación acordada y documentada,
sin incluirlos en el historial Git convencional.
