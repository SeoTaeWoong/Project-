import cv2
import socket
import numpy as np
import time
serverIP = '192.168.137.1'
serverPORT = 8485
cam = cv2.VideoCapture(0)
cam.set(3,320)
cam.set(4,240)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        sock.connect((serverIP, serverPORT))
        while True:
            ret, frame = cam.read()
            if ret:
                result, frame = cv2.imencode('.jpg', frame, encode_param)
                data = np.array(frame)
                stringData = data.tostring()
                sock.sendall((str(len(stringData))).encode().ljust(16) + stringData)

while True:
    try:
        run()
    except Exception as ex:
        time.sleep(2)
        print(ex)
