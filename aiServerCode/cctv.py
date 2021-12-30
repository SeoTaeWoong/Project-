import cv2
import socket
import numpy as np

while True:
   
    try:
        cam  = cv2.VideoCapture(-1)
        cam.set(3,640);
        cam.set(4,480);
        while cam.isOpened():
            ret, frame = cam.read()
            print(cam.isOpened())
            if ret:
                cv2.imshow("test", frame)
                cv2.waitKey(1)
    except Exception as e:
        cam.release()
        cv2.destroyAllWindows()
        print(e)
        print("error")
