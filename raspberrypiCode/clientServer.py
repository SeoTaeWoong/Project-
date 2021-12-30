import socket
import numpy as np
import cv2
import threading as Threading
import millis
import json
import base64
import time


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
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            self.serverIP = '192.168.1.216'
            self.serverPORT = 8485
            self.cam = cv2.VideoCapture(1)
            self.cam.set(3,320)
            self.cam.set(4,240)
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
            if(getData["type"] == "request/RobotSettings" and getData["origin"] == "rasp"):
                print(getData)
                message = self.__messageForm
                message["destination"] = self.serverIP
                message["type"] = "response/RobotSettings"
                message["data"] = "ok"
                self.sendMSG(ser_socket, message)
                
                #여기서 웹으로 데이터 전송 코드 작성하기
                #
                #
                
            elif(getData["type"] == "request/RealTimeStatus" and getData["origin"] == "rasp"):
                print(getData)
                message = self.__messageForm
                message["destination"] = self.serverIP
                message["type"] = "response/RealTimeStatus"
                message["data"] = "ok"
                self.sendMSG(ser_socket, message)
                
                #여기서 웹으로 데이터 전송 코드 작성하기
                #
                #
            
                
            elif(getData["type"] == "response/BluetoothConnection" and getData["origin"] == "rasp"):
                print(getData)
                
                #블루투스 연결 성공 웹으로 데이터 전송코드 작성하기
                
            elif(getData["type"] == "request/RobotSettingModify" and getData["origin"] == "aiServer"):
                print(getData)
                message = self.__messageForm
                message["destination"] = self.serverIP
                message["type"] = "response/RobotSettingModify"
                message["data"] = "ok"
                self.sendMSG(ser_socket, message)
                # 수정된 로봇데이터를 라즈베리파이에 전송
                
            elif(getData["type"] == "request/RobotControll" and getData["origin"] == "web"):
                print(getData)
                
                #로봇 컨트롤 값을 라즈베리파이에 전송 (web모드)
                #응답 필요없음
    
    def realTimeStatusThread(self, ser_socket):
        while True:
            try:
                ret, frame = self.cam.read()
                print(ret)
                if ret:
                    result, frame = cv2.imencode('.jpg', frame, self.encode_param)
                    imgData = np.array(frame)
                    stringData = imgData.tostring()
                    base64Data = self.byteTransformBase64(stringData)
                    realTimeData = {"pwm":"1","deg":"1","img":base64Data}
                    message = self.__messageForm
                    message["destination"] = self.serverIP
                    message["type"]="request/RealTimeStatus"
                    message["data"]=realTimeData
                    self.sendMSG(ser_socket, message)
                    getData = self.recvMSG(ser_socket)
                    if(getData["type"] == "response/RealTimeStatus") and (getData["data"] == "ok"):
                        print("realtimedata send ok")
                        
            except Exception as e:
                print(e)
                time.sleep(5)
            
    
    def transferData(self, ser_socket):
        self.connectionCheck(ser_socket)
        print("cli conn ok")
        
        # robot 기본 셋팅정보 가져오기
        # 시리얼로 요청함수 작성 일단 임시코드 사용 추후 수정해야함
        rsCheck = True
        while rsCheck:
            robotData = self.getRobotSettings()
            message = self.__messageForm
            message["destination"] = self.serverIP
            message["type"] = "request/RobotSettings"
            message["data"] = robotData
            self.sendMSG(ser_socket, message)
            while rsCheck:
                getData = self.recvMSG(ser_socket)
                if(getData["type"] == "response/RobotSettings" and getData["data"] == "ok"):
                    print("ok")
                    print("wait")
                    rsCheck = False
                    
        threadSend = Threading.Thread(target=self.realTimeStatusThread, args=(ser_socket,))
        threadSend.start()
        
        while True:
            time.sleep(2)
            print("while~~")
                
                
    def clientON(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((self.serverIP, self.serverPORT))
            print("gogo")
            self.transferData(sock)

while True:
    try:
        a = SocketClient()
        a.clientON()
    except Exception as ex:
        time.sleep(2)
        print(ex)
