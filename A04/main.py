import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # type: ignore
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml') # type: ignore

cap = cv2.VideoCapture(0) # 0 significa la cámara por defecto

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for(x, y, w, h) in faces: 
        roi_gray = gray[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
    
        if len(smiles) > 0:
           cv2.putText(frame, 'Sonriendo', (x, y - 10),
           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
           boca_y = y + int(h * 0.84)
           cv2.circle(frame, (x + w//2, mouth_y), 40, (0, 0, 255), 2)  # circulo
           #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # rectangulo

        else:
            cv2.putText(frame, 'Serio', (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            mouth_y = y + int(h * 0.84)
            cv2.circle(frame, (x + w//2, mouth_y), 40, (0, 0, 255), 2)  # circulo
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # rectangulo
    
    cv2.imshow('Detector de Sonrisas', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #Liberar la cámara y cerrar las ventanas
    # #cap.release()
    # #cv2.destroyAllWindows