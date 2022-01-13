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
        print("읽기")
        while True:
            getData = self.recvMSG(cli_socket, addr)
                
                
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

