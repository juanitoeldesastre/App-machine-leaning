import cv2
import numpy as np
from keras.applications.mobilenet import MobileNet, decode_predictions, preprocess_input
from keras.preprocessing.image import img_to_array

# Capturar imagen
cap = cv2.VideoCapture(0)
print("Presiona ESPACIO para capturar una imagen")

while True:
    ret, frame = cap.read()
    cv2.imshow("Webcam - Presiona ESPACIO para capturar", frame)
    key = cv2.waitKey(1)

    if key == 27:  # ESC
        cap.release()
        cv2.destroyAllWindows()
        exit()
    elif key == 32:  # ESPACIO
        image = frame
        break

cap.release()
cv2.destroyAllWindows()

# Preprocesamiento
resized_image = cv2.resize(image, (224, 224))
image_array = img_to_array(resized_image)
image_array = np.expand_dims(image_array, axis=0)
image_array = preprocess_input(image_array)

# Modelo y predicción
model = MobileNet(weights='imagenet')
predictions = model.predict(image_array)
decoded = decode_predictions(predictions, top=3)[0]

# Mostrar resultados
for i, (imagenetID, label, prob) in enumerate(decoded):
    print(f"{i+1}. {label}: {prob*100:.2f}%")
