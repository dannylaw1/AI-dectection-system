import cv2

phone_cascade = cv2.CascadeClassifier('haarcascade_phone.xml')

def detect(gray, frame):
    phones = phone_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in phones:
        if not (w < 100 or h < 100):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.rectangle(frame, (x+int(w/2), y+int(h/2)), (x+int(w/2)+10, y+int(h/2)+10), (0, 0, 255), 2) # center
    return frame

# Open a video capture stream (0 for webcam or provide a video file path)
cap = cv2.VideoCapture(0)  # Change to the appropriate video source

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canvas = detect(gray, frame)
    
    cv2.imshow('Phone Detection', canvas)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
