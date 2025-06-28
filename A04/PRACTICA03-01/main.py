import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

# Encender la cámara
webcam = cv2.VideoCapture(0)

# Procesar cada cuadro (frame) en tiempo real
while True:
    status, frame = webcam.read()

    if not status:
        break

    # Detectar objetos
    bbox, label, conf = cv.detect_common_objects(frame)

    # Dibujar las cajas con etiquetas
    output = draw_bbox(frame, bbox, label, conf)

    # Mostrar el video con los objetos detectados
    cv2.imshow("Object Detection", output)

    # Salir del programa con una tecla
    if cv2.waitKey(1) == 27:
        break

# Liberar recursos
webcam.release()
cv2.destroyAllWindows()
