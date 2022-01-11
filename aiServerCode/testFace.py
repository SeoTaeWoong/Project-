import cv2 
import numpy as np


faceCascade = cv2.CascadeClassifier(".\haar\haarcascade_frontalface_default.xml")
#faceCascade = cv2.CascadeClassifier('D:\project2021\Project-\aiServerCode\haar\haarcascade_frontalface_default.xml')


def detect(gray,frame):
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w, y+h), (255,0,0),2)
        
        face_gray = gray[y:y+ h, x:x + w]
        face_color = frame[y:y + h, x:x + w]
    
    return frame

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read() 
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canvas = detect(gray, frame)
        
        cv2.imshow('result',canvas)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()        