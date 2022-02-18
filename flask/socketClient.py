import socket
import numpy as np
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
            cls._init = True
    

    def sendMSG(self, ser_socket, message):
        jsonData = json.dumps(message)
        jsonLength = self.jsonTransformByteLength(jsonData)
        ser_socket.sendall(jsonLength+jsonData.encode())
    
    def recvMSG(self, ser_socket):

        try :
            msgLength = ser_socket.recv(16)
            if msgLength :
                msgLength  = int(msgLength.decode())
                msgData = b''
                while msgLength:
                    newBuf = ser_socket.recv(msgLength)
                    if not newBuf : 
                        return None
                    msgData += newBuf
                    msgLength -= len(newBuf)
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
            try:
                getData = self.recvMSG(ser_socket)
                if(getData["type"] == "request/RobotSettings" and getData["origin"] == "aiServer"):
                    
                    message = self.__messageForm
                    message["destination"] = self.serverIP
                    message["type"] = "response/RobotSettings"
                    message["data"] = "ok"
                    self.sendMSG(ser_socket, message)
                    
                    
    
                elif(getData["type"] == "request/RealTimeStatus" and getData["origin"] == "aiServer"):
                    roadCam = self.base64TransformByte(getData["data"]["roadCam"])
                    humanCam = self.base64TransformByte(getData["data"]["humanCam"])
                    warning = getData["data"]["warning"]
                    if self.imgQue1.qsize() >10:
                        self.imgQue1.get()
                        self.imgQue1.put(roadCam)
                    else :
                        self.imgQue1.put(roadCam)

                    if self.imgQue2.qsize() >10:
                        self.imgQue2.get()
                        self.imgQue2.put(humanCam)
                    else :
                        self.imgQue2.put(humanCam)
                        
                    if self.warningQue.qsize() >10:
                        self.warningQue.get()
                        self.warningQue.put(warning)
                    else :
                        self.warningQue.put(warning)
                    
                elif(getData["type"] == "response/BluetoothConnection" and getData["origin"] == "aiServer"):
                    print(getData)
                    
                    #블루투스 연결 성공 웹으로 데이터 전송코드 작성하기
                    
                elif(getData["type"] == "request/RobotControll" and getData["origin"] == "web"):
                    print(getData)
                    
                    #로봇 컨트롤 값을 라즈베리파이에 전송 (web모드)
                    #응답 필요없음
            except Exception as e:
                print("get error:",e)
    
    def realTimeStatusThread(self, ser_socket):
        pass
            
    
    def transferData(self, ser_socket):
        self.connectionCheck(ser_socket)
        print("cli conn ok")
        
        # robot 기본 셋팅정보 가져오기
        # 시리얼로 요청함수 작성 일단 임시코드 사용 추후 수정해야함
        self.recvThread(ser_socket)
        
                
    def clientON(self,imgQueue1, imgQueue2, robotDataQueue, setDataQueue, warningQue):
        self.imgQue1 = imgQueue1
        self.imgQue2 = imgQueue2
        self.warningQue = warningQue
        self.robotDataQue = robotDataQueue
        self.setDataQueue = setDataQueue
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((self.serverIP, self.serverPORT))
            print("gogo")
            self.transferData(sock)
