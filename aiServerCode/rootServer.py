import socket
import numpy as np
import cv2
import threading as Threading
import millis
import json


class SocketServer(object):
    __socket = ""
    __socketList = []
    __robotData = {}

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

    def deleteSocket(self, cli_socket):
        with Threading.Lock():
            for socket in self.__socketList[:]:
                if socket["cli_sock"] == cli_socket:
                    print("스레드 종료")
                    self.__socketList.remove(socket)
                    return True
        return False



    def recvall(sock, count):
        # 바이트 문자열
        buf = b'' 
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def transferData(self, cli_socket, addr):
        timer = millis.Millis()
        now = 0

        sendMessage = {"origin":"aiServer",
                       "destination":addr[0],
                       "type":"request/purpose",
                       "data":""}
        jsonData = json.dumps(sendMessage)
        cli_socket.sendall(jsonData.encode())

        connCheck = True
        while connCheck:
            data = cli_socket.recv(1024)
            if data == bytes(b''):
                now = millis.Millis()
                if ((now-timer)/1000 > 50):
                    if self.deleteSocket(cli_socket):
                        return
            else:
                timer = millis.Millis()
                data = json.loads(data)
                print("test1",data)
                if data["type"] == "response/purpose":
                    for socket in self.__socketList:
                        if socket["addr"] == data["origin"]:
                            socket["hostName"] = data["data"]
                            sendMessage["destination"] = data["data"]
                            socket["connection"] = "on"
                            connCheck = False
                            break
        if sendMessage["destination"] == "raspberryPi":
            self.rasp_server(cli_socket, sendMessage)
        elif sendMessage["destination"] == "webServer":
            print 
                
    def rasp_server(self, cli_socket, sendMessage):
        timer = millis.Millis()
        now = 0
        while True:
            data = cli_socket.recv(1024)
            if data == bytes(b''):
                now = millis.Millis()
                if ((now-timer)/1000 > 50):
                    if self.deleteSocket(cli_socket):
                        return
            else:
                timer = millis.Millis()
                data = json.loads(data)
                if data["type"] == "request/robotData":
                    self.__robotData = data
                    sendMessage["origin"] = "aiServer"
                    sendMessage["destination"] = data["origin"]
                    sendMessage["type"] = "response/robotData"
                    sendMessage["data"] = "ok"
                    jsonData = json.dumps(sendMessage)
                    cli_socket.sendall(jsonData.encode())
                    break
        
        while True:
            data = cli_socket.recv(65535)
            if data == bytes(b''):
                now = millis.Millis()
                if ((now-timer)/1000 > 50):
                    if self.deleteSocket(cli_socket):
                        return
            else:
                timer = millis.Millis()
                print(type(data))
                if type(data) == str:
                    data = json.loads(data)
                    if data["type"] == "liveData":
                        print("결과 : " ,data)
                elif type(data) == bytes:
                    while True:
                        print("??")
                    # client에서 받은 stringData의 크기 (==(str(len(stringData))).encode().ljust(16))
                        len = self.recvall(cli_socket, 16)
                        stringData = self.recvall(cli_socket, int(len))
                        
                        
                        data = np.fromstring(stringData, dtype = 'uint8')
                        #data를 디코딩한다.
                        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

                        cv2.imshow("frameName",frame)
                        cv2.waitKey(1)

                   
        

    def serverON(self):
        while True:
            try:
                if len(self.__socketList) >= 3:
                    continue
                cli_socket, addr = self.__socket.accept()
                self.__socketList += [{"cli_sock":cli_socket,"addr":addr[0],"port":addr[1],"hostName":"","connection":"off"}]
                print("연결!!!!!!!!!!!!!!")
            except KeyboardInterrupt:
                self.__socket.close()
                print("Keyboard interrupt")
            
            tData = Threading.Thread(target=self.transferData, args=(cli_socket, addr))
            tData.start()



a = SocketServer()
a.serverON()

