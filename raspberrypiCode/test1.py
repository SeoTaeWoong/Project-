import cv2
import socket
import numpy as np

cam  = cv2.VideoCapture(0)

cam.set(3,320);
cam.set(4,240);


while True:
    ret, frame = cam.read()
    if ret:
        cv2.imshow("test", frame)

        if cv2.waitKey(1) and 0xFF ==

cam.release()

