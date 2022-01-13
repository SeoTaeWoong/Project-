import socket
import numpy as np
import cv2
import threading as Threading
import millis
import json
import base64
import time
import raspAtmegaSerial
from multiprocessing import Process, Queue
import warnings
warnings.filterwarnings('ignore')


class SocketClient(object):
    __socket = ""
    __socketList = []
    __robotData = {}
    __messageForm = {"origin":"rasp",
                   "destination":"",
                   "type":"request/purpose",
                   "data":""}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, robotQueue):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            self.robotQueue = robotQueue
            self.serverIP = '192.168.137.1'
            self.serverPORT = 8485
            self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            cls._init = True
    
    def sendMSG(self, ser_socket, message):
        jsonData = json.dumps(message)
        jsonLength = self.jsonTransformByteLength(jsonData)
        ser_socket.sendall(jsonLength+jsonData.encode())
    
    def recvMSG(self, ser_socket):
        
        while True:
            try :
                msgLength = ser_socket.recv(16)
                msgLength  = int(msgLength.decode())
                msgData = ser_socket.recv(msgLength)
                return json.loads(msgData)
            except Exception as e:
                print("err3:",e)
                while True:
                    bufferClear = ser_socket.recv(1024)
                    if not bufferClear:
                        self.requestReply(ser_socket)
                        break
    
    def requestReply(self, ser_socket):
        message = self.__messageForm
        message["destination"] = self.serverIP
        message["type"] = "request/reply"
        message["data"] = "data seq err"
        self.sendMSG(ser_socket, message)
    
    def jsonTransformByteLength(self, jsonData):
        return str(len(jsonData)).encode().ljust(16)
        
    def byteTransformBase64(self, frame):
        encoded = base64.b64encode(frame)
        return encoded.decode("ascii")
    
    def base64TransformByte(self, frame):
        decoded = base64.b64decode(frame)
        return decoded
    
    def realTimeStatusThread2(self,id, ser_socket, robotQueue, tempQueue):
        while True:
            message = "hi zzz"
            tempQueue.put(type(ser_socket))
            tempQueue.put(ser_socket)
            self.sendMSG(ser_socket, message)
            time.sleep(2)
            

                    
   
    def realTimeStatusThread(self,id, ser_socket, robotQueue, tempQueue):
        comparativeData = self.comparative
        tempQueue.put(comparativeData)
        while True:
            cam = cv2.VideoCapture(-1)
            #cam.set(3,320)
            #cam.set(4,240)
            if cam.isOpened():
                tempQueue.put(cam.isOpened())
            while cam.isOpened():
                try:
                    ret, frame = cam.read()
                    if ret:
                        if robotQueue.qsize == 1:
                            robotData = robotQueue.get()
                            if comparativeData != robotData:
                                comparativeData = robotData
                        elif robotQueue.qsize == 0:
                            robotData = comparativeData
                        tempQueue.put("robotData:", robotData)
                        result, frame = cv2.imencode('.jpg', frame, self.encode_param)
                        imgData = np.array(frame)
                        byteData = imgData.tobytes()
                        base64Data = self.byteTransformBase64(byteData)
                        realTimeData = robotData
                        tempQueue.put("robotData:", base64Data[:30])
                        if realTimeData["type"] == "responseData":
                            del(realTimeData["type"])
                            realTimeData["img"] = base64Data
                        else:
                            realTimeData = {"img":base64Data}
                        message = self.__messageForm
                        message["destination"] = self.serverIP
                        message["type"]="request/RealTimeStatus"
                        message["data"]=realTimeData
                        self.sendMSG(ser_socket, message)
                        # getData = self.recvMSG(ser_socket)
                        # if(getData["type"] == "response/RealTimeStatus") and (getData["data"] == "ok"):
                        #     print("realtimedata send ok")        
                except Exception as e:
                    cam.release()
                    cv2.destroyAllWindows()
                    #print("err1:",e)
                    
                
            
    
    def transferData(self, ser_socket):
       
        tempQueue = Queue()
        processSend = Process(target=self.realTimeStatusThread2, args=(1, ser_socket, self.robotQueue, tempQueue))
        processSend.start()
        print("3Round")
        while True:
            if tempQueue.qsize() != 0:
                print(tempQueue.get())
            pass

    def clientON(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((self.serverIP, self.serverPORT))
            print("gogo")
            self.transferData(sock)


while True:
    try:
        robotQueue = Queue()

        raspCLI_aiSER = SocketClient(robotQueue)
        raspCLI_aiSER.clientON()
    except Exception as ex:
        print("err2:",ex)
