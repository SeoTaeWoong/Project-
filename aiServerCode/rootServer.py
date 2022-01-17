import socket
import numpy as np
import cv2
import threading as Threading
import millis
import json
import base64


class SocketServer(object):
    __socket = ""
    __socketList = []
    __robotData = {}
    __messageForm = {"origin":"aiServer",
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
            self.__socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.__socket.bind(("",8485))
            self.__socket.listen(5)
            cls._init = True
    
    def sendMSG(self, cli_socket, message):
        jsonData = json.dumps(message)
        jsonLength = self.jsonTransformByteLength(jsonData)
        cli_socket.sendall(jsonLength+jsonData.encode())
    
    def recvMSG(self, cli_socket, addr):
        
        while True:
            try :
                msgLength = cli_socket.recv(16)
                if msgLength :
                    msgLength  = int(msgLength.decode())
                    msgData = b''
                    while msgLength:
                        newBuf = cli_socket.recv(msgLength)
                        if not newBuf : 
                            return None
                        msgData += newBuf
                        msgLength -= len(newBuf)
                    return json.loads(msgData)
            except Exception as e:
                print(e)
                print("들어옴")
                while True:
                    bufferClear = cli_socket.recv(1024)
                    if not bufferClear:
                        self.requestReply(cli_socket, addr)
                        break
    
    def requestReply(self, cli_socket, addr):
        message = self.__messageForm
        message["destination"] = addr[0]
        message["type"] = "request/reply"
        message["data"] = "data seq err"
        self.sendMSG(cli_socket, message)
    
    def jsonTransformByteLength(self, jsonData):
        return str(len(jsonData)).encode().ljust(16)
        
    def imgTransformBase64(self, frame):
        encoded = base64.b64encode(frame)
        return encoded.decode("ascii")
    
    def base64TransformImg(self, frame):
        decoded = base64.b64decode(frame)
        return decoded
    
    def connectionCheck(self, cli_socket, addr):
        
        while True:
            getData = self.recvMSG(cli_socket, addr)
            if getData["type"] == "request/ThreeWayHandShake#1":
                message = self.__messageForm
                message["destination"] = addr[0]
                message["type"] = "response/ThreeWayHandShake#2"
                message["data"] = "response 'ACK' to request 'SYN' MSG"
                self.sendMSG(cli_socket, message)
                message = self.__messageForm
                message["destination"] = addr[0]
                message["type"] = "request/ThreeWayHandShake#3"
                message["data"] = "request 'SYN' MSG"
                self.sendMSG(cli_socket, message)
                getData = self.recvMSG(cli_socket, addr)
                if getData["type"] == "response/ThreeWayHandShake#4":
                    if getData["data"] == "response 'ACK' to request 'SYN' MSG":
                        print(getData)
                        return 
    
    
    
    def transferData(self, cli_socket, addr):
        self.connectionCheck(cli_socket, addr)
        print(addr[0],"커넥션 완료")
        while True:
            getData = self.recvMSG(cli_socket, addr)
            if(getData and getData["type"] == "request/RobotSettings" and getData["origin"] == "rasp"):
                message = self.__messageForm
                message["destination"] = addr[0]
                message["type"] = "response/RobotSettings"
                message["data"] = "ok"
                self.sendMSG(cli_socket, message)
                print("robotSettings 응답 완료")
                print("받은 데이터 ", getData)
                #여기서 웹으로 데이터 전송 코드 작성하기
                #
                #
                
            elif(getData and getData["type"] == "request/RealTimeStatus" and getData["origin"] == "rasp"):
                message = self.__messageForm
                message["destination"] = addr[0]
                message["type"] = "response/RealTimeStatus"
                message["data"] = "ok"
                self.sendMSG(cli_socket, message)
                print("응답 성공: ")
                frame1 = self.base64TransformImg(getData["data"]['img'])
                frame2 = self.base64TransformImg(getData["data"]['img2'])
                
                frameData1 = np.frombuffer(frame1, dtype = 'uint8')
                frameData2 = np.frombuffer(frame2, dtype = 'uint8')
                #data를 디코딩한다.
                frame1 = cv2.imdecode(frameData1, cv2.IMREAD_COLOR)
                frame2 = cv2.imdecode(frameData2, cv2.IMREAD_COLOR)
                frame1 = cv2.flip(frame1,0)
                cv2.imshow("frameName",frame1)
                cv2.imshow("frameName2",frame2)
                cv2.waitKey(1)
                for key,value in getData["data"].items():
                    if key != "img" or key != "img2":
                        print(key, value)
                #여기서 웹으로 데이터 전송 코드 작성하기
                #
                #
            
                
            elif(getData and getData["type"] == "response/BluetoothConnection" and getData["origin"] == "rasp"):
                print(getData)
                
                #블루투스 연결 성공 웹으로 데이터 전송코드 작성하기
                
            elif(getData and getData["type"] == "request/RobotSettingModify" and getData["origin"] == "web"):
                print(getData)
                message = self.__messageForm
                message["destination"] = addr[0]
                message["type"] = "response/RobotSettingModify"
                message["data"] = "ok"
                self.sendMSG(cli_socket, message)
                # 수정된 로봇데이터를 라즈베리파이에 전송
                
            elif(getData and getData["type"] == "request/RobotControll" and getData["origin"] == "web"):
                print(getData)
                cv2.VideoCapture()
                #로봇 컨트롤 값을 라즈베리파이에 전송 (web모드)
                #응답 필요없음
               
                
                
    def serverON(self):
        while True:
            try:
                if len(self.__socketList) >= 10:
                    continue
                print("??")
                cli_socket, addr = self.__socket.accept()
                self.__socketList += [{"cli_sock":cli_socket,"addr":addr[0],"port":addr[1],"hostName":"","connection":"off"}]
                print("연결!!!!!!!!!!!!!!")
                tData = Threading.Thread(target=self.transferData, args=(cli_socket, addr))
                tData.start()
            except KeyboardInterrupt:
                self.__socket.close()
                print("Keyboard interrupt")
            
            



a = SocketServer()
a.serverON()

