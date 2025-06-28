# **Documentación**

## **Descripción**

Este proyecto utiliza un entorno virtual de Python y las bibliotecas **OpenCV**, **cvlib** y **TensorFlow** para realizar detección de objetos. Durante la configuración e instalación, hubo un inconveniente al intentar descargar automáticamente el modelo **YOLOv3**, lo que resultó en un error. Sin embargo, se resolvió manualmente descargando los archivos necesarios de **YOLOv4** desde el repositorio oficial.

### **Pasos Seguidos:**

1. **Creación del entorno virtual en Python**:
   Para crear un entorno virtual de Python, se utilizó el siguiente comando:

   ```bash
   python -m venv tf_env
   ```

2. **Instalación de las bibliotecas necesarias**:
   Las librerías esenciales fueron instaladas en el entorno virtual usando `pip`:

   ```bash
   pip install opencv-python cvlib tensorflow
   ```

   Esto permite utilizar OpenCV para procesamiento de imágenes, **cvlib** para detección de objetos y **TensorFlow** para el entrenamiento y ejecución del modelo de aprendizaje automático.

3. **Integración del código**:
   Se agregó el código necesario para realizar la detección de objetos, sin problemas, hasta la parte en que se intentó descargar **YOLOv3** de forma automática.

4. **Problema con la descarga automática de YOLO**:
   Durante el proceso de descarga automática de **YOLOv3** por parte del código, se cortó la conexión a Internet, lo que provocó que la descarga no se completara correctamente. Aunque el programa reconoció la presencia de **YOLOv3**, los archivos descargados estaban incompletos.

   **Solución:**

   * Se localizó la carpeta **`C:\Users\ETIA\.cvlib\object_detection\yolo\yolov3`**.
   * Se eliminaron todos los archivos incompletos en esta ruta.
   * Posteriormente, se descargaron manualmente los archivos necesarios: **`yolov4.cfg`** y **`yolov4.weights`** desde el repositorio original de **YOLOv4**.

5. **Repositorio de YOLOv4**:
   Los archivos completos de **YOLOv4** se descargaron desde el repositorio oficial:

   * [Repositorio YOLOv4 Darknet](https://github.com/kiyoshiiriemon/yolov4_darknet)

   Los archivos a descargar son:

   * **`yolov4.cfg`**
   * **`yolov4.weights`**

   **Importante**: Estos archivos deben ser ubicados en la carpeta **`C:\Users\ETIA\.cvlib\object_detection\yolo\yolov3`**, para que el código de detección de objetos funcione correctamente.

6. **Código Final**:
   El código fue dejado tal y como estaba originalmente, sin modificaciones, y ahora se ejecuta correctamente con los archivos de **YOLOv4**.

---

### **Versiones:**

* **Python 3.10**
* **YOLOv4** (Tambien funciona con YOLOV3)

---

### **Solución**

Hubo un inconveniente con la descarga automática de **YOLOv3**, pero este problema fue solucionado manualmente descargando los archivos **`yolov4.cfg`** y **`yolov4.weights`** desde el repositorio original. Ahora el sistema está funcionando correctamente.
