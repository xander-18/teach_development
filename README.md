Detección de Objetos en Tiempo Real con YOLOv3-Tiny
Este proyecto realiza la detección de objetos en tiempo real usando YOLOv3-tiny y la biblioteca cvlib de Python. La aplicación se puede ejecutar directamente en Python o compilarse como un ejecutable .exe.

Requisitos
Python 3.7 o superior: Puedes descargarlo desde python.org.
PyInstaller: para convertir el script Python en un ejecutable.
Librerías de Python
Instala las librerías necesarias ejecutando:

opencv-python-headless
cvlib
numpy
requests
pathlib

Descarga de YOLOv3-tiny
El script main.py incluye una función download_yolo_tiny() que descarga automáticamente los archivos de configuración y pesos del modelo YOLOv3-tiny. No necesitas descargarlos manualmente; el script los descarga en la primera ejecución.

Ejecución del Script en Python
Para ejecutar el proyecto en modo desarrollo, usa:

python detection.py
Este comando inicia la detección de objetos usando tu cámara conectada.

Crear el Ejecutable .exe con PyInstaller
Instalación de PyInstaller
Primero, instala PyInstaller si aún no lo tienes:

pip install pyinstaller
Creación del Ejecutable
Para crear el ejecutable, ejecuta el siguiente comando desde el directorio del proyecto:

pyinstaller --onefile --windowed <tuarchivo>.py
Opciones:
--onefile: Crea un único archivo .exe en lugar de varios archivos.
--windowed: Oculta la consola cuando se ejecuta el ejecutable. Si prefieres ver la consola, puedes omitir esta opción.
Esto generará un archivo ejecutable en la carpeta dist.

Notas adicionales
Si el ejecutable no encuentra los archivos de configuración y pesos del modelo YOLO, asegúrate de ejecutar el script en Python al menos una vez para descargar estos archivos. El script guardará los archivos en el directorio ~/.cvlib/yolo-tiny.

Uso del Ejecutable
Navega a la carpeta dist que contiene el archivo main.exe.
Haz doble clic en main.exe o ejecútalo desde la terminal para iniciar la detección de objetos en tiempo real.
Para salir de la aplicación, presiona la tecla q.

Este README.md proporciona una guía detallada de cómo configurar y ejecutar el proyecto, así como las instrucciones para crear el archivo ejecutable.
