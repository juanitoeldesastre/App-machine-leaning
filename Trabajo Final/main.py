# Importar la librería de OpenCV
import cv2

# Cargar los clasificadores en cascada pre-entrenados
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Captura de video desde la cámara web por defecto
cap = cv2.VideoCapture(0)

# Verificamos si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error la cámara no inicio.")
    exit()

# Bucle infinito para leer los frames del video
while True:
    # Leer un frame de la cámara
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame.")
        break

    # Convertir el frame a escala de grises
    # Los algoritmos de detección de Haar Cascade funcionan mejor y más rápido en imágenes en escala de grises.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en la imagen en escala de grises
    # detectMultiScale() detecta objetos de diferentes tamaños en la imagen de entrada.
    # - scaleFactor: Reduce el tamaño de la imagen en un 30% en cada paso.
    # - minNeighbors: Especifica cuántos "vecinos" debe tener cada rectángulo candidato para ser retenido.
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Iterar sobre cada rostro detectado
    # y (w, h) son el ancho (width) y el alto (height) del rectángulo.
    for (x, y, w, h) in faces:
        
        # Definir la Region of Interest (ROI)
        # Para optimizar la búsqueda de ojos, solo buscamos dentro del área del rostro.
        # Creamos una ROI tanto en la imagen en escala de grises como a color.
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detectar ojos dentro de la ROI del rostro
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)

        # Iterar sobre cada ojo detectado
        # (ex, ey, ew, eh) son las coordenadas del ojo RELATIVAS a la ROI del rostro.
        for (ex, ey, ew, eh) in eyes:

            # Dibujar un círculo sobre el ojo
            centro_x = ex + ew // 2
            centro_y = ey + eh // 2
            radio = int((ew + eh) / 4)
            cv2.circle(roi_color, (centro_x, centro_y), radio, (255, 0, 0), 2)

    cv2.imshow('Deteccion de Ojos', frame)

    # Condición para salir del bucle con la 'q'.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break # Romper el bucle

# Libera la cámara web.
cap.release()
# Cierra todas las ventanas creadas por OpenCV.
cv2.destroyAllWindows()