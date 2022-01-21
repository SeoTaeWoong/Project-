import socket
import numpy as np
import cv2
import threading as Threading
#import millis
import json
import base64
import time


class SocketClient(object):
    __socket = ""
    __socketList = []
    __robotData = {}
    __messageForm = {"origin":"web",
                   "destination":"",
                   "type":"request/purpose",
                   "data":""}

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            self.serverIP = '121.139.165.163'
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
                print(msgData)
                return json.loads(msgData)
            except Exception as e:
                print(e)
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
    
    def connectionCheck(self, ser_socket):
        while True:
            message = self.__messageForm
            message["destination"] = self.serverIP
            message["type"] = "request/ThreeWayHandShake#1"
            message["data"] = "request 'SYN' MSG"
            self.sendMSG(ser_socket, message)
            getData = self.recvMSG(ser_socket)
            if getData["type"] == "response/ThreeWayHandShake#2" and getData["data"] == "response 'ACK' to request 'SYN' MSG":
                getData = self.recvMSG(ser_socket)
                if getData["type"] == "request/ThreeWayHandShake#3":
                    message = self.__messageForm
                    message["destination"] = self.serverIP
                    message["type"] = "response/ThreeWayHandShake#4"
                    message["data"] = "response 'ACK' to request 'SYN' MSG"
                    self.sendMSG(ser_socket, message)
                    return 
    
    def getRobotSettings(self):
        robotData = {
                    "Controller":"auto",
                    "MaxSPD":"160",
                    "MinSPD":"0",
                    "Kp":"1",
                    "Ki":"0",
                    "Kd":"0"
                    }
        return robotData
    
    def recvThread(self, ser_socket):
        while True:
            getData = self.recvMSG(ser_socket)
            print(getData)
            if(getData["type"] == "request/RobotSettings" and getData["origin"] == "aiServer"):
                print(getData)
                message = self.__messageForm
                message["destination"] = self.serverIP
                message["type"] = "response/RobotSettings"
                message["data"] = "ok"
                self.sendMSG(ser_socket, message)
                
                
   
            elif(getData["type"] == "request/RealTimeStatus" and getData["origin"] == "aiServer"):
                print(getData)
                self.imgQue1.put(getData["data"]['roadCam'])
                self.imgQue2.put(getData["data"]['humanCam'])
                
            elif(getData["type"] == "response/BluetoothConnection" and getData["origin"] == "aiServer"):
                print(getData)
                
                #블루투스 연결 성공 웹으로 데이터 전송코드 작성하기
                
            elif(getData["type"] == "request/RobotControll" and getData["origin"] == "web"):
                print(getData)
                
                #로봇 컨트롤 값을 라즈베리파이에 전송 (web모드)
                #응답 필요없음
    
    def realTimeStatusThread(self, ser_socket):
        pass
            
    
    def transferData(self, ser_socket):
        self.connectionCheck(ser_socket)
        print("cli conn ok")
        
        # robot 기본 셋팅정보 가져오기
        # 시리얼로 요청함수 작성 일단 임시코드 사용 추후 수정해야함
        self.recvThread()
        
                
    def clientON(self,imgQueue1, imgQueue2, robotDataQueue, setDataQueue):
        self.imgQue1 = imgQueue1
        self.imgQue2 = imgQueue2
        self.robotDataQue = robotDataQueue
        self.setDataQueue = setDataQueue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((self.serverIP, self.serverPORT))
            print("gogo")
            self.transferData(sock)

while True:
    try:
        a = SocketClient()
        a.clientON() #이걸 멀티프로세스로 실행
    except Exception as ex:
        time.sleep(2)
        print(ex)
