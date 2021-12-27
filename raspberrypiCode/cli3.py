import cv2
import socket
import numpy as np
import time
<<<<<<< HEAD
import millis
import json

serverIP = '192.168.1.86'
=======
localhost = "127.0.0.1"
serverIP = '192.168.137.1'
>>>>>>> 099004b3984dcde0fe624920d1b444aa4e2c74de
serverPORT = 8485
cam = cv2.VideoCapture(0)
cam.set(3,320)
cam.set(4,240)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        sock.connect((localhost, serverPORT))
        while True:
            data = sock.recv(1024)
            data = json.loads(data)
            print(data)
            if data["origin"] == "aiServer" and data["type"] =="request/purpose":
                tmpOrigin = data["origin"]
                data["origin"] = data["destination"]
                data["destination"] = tmpOrigin
                data["type"] = "response/purpose"
                data["data"] = "raspberryPi"
                jsonData = json.dumps(data)
                sock.sendall(jsonData.encode())
                data["origin"] = data["data"]
                break

        #getdata-> atmega(maxspd,minspd,controller,kp,ki,kd)
        data["type"] = "request/robotData"
        data["data"] = {"maxspd":160,"minspd":50,"controller":"auto"
                        ,"kp": 1,"ki":2,"kd":1}
        jsonData = json.dumps(data)
        sock.sendall(jsonData.encode())
        while True:
            del data
            data = sock.recv(1024)
            data = json.loads(data)
            if data["origin"] == "aiServer" and data["type"] == "response/robotData":
                if data["data"] == "ok":
                    print("robotCheck")
                    break 
        timer = millis.Millis()
        sendMessage = {
                "origin":"raspberryPi",
                "destination":"webServer",
                "type":"",
                "data":""
                }
        while True:
            ret, frame = cam.read()
            if ret:
                now = millis.Millis()
                if (now-timer)%60 == 0:
                    timer = now
                    result, frame = cv2.imencode('.jpg', frame, encode_param)
                    imgData = np.array(frame)
                    stringData = imgData.tostring()
                    jsonData = json.dumps(sendMessage)
                    sock.sendall(str(len(stringData)).encode().ljust(16)+stringData)

while True:
    try:
        run()
    except Exception as ex:
        time.sleep(2)
        print(ex)
