from multiprocessing.process import current_process
import socket
import numpy as np
import cv2
import threading as Threading
import millis
import json
import base64
import time
import raspAtmegaSerial
from multiprocessing import Process, Queue, Pipe
import controller as Joycon
import warnings
import humanCam as HumanCam
import edge as Edge
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
    
    def __init__(self, robotQueue,setDataQueue,cmdDataQueue,serialParentPipe,hCamQueue,joyParentPipe):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            self.robotQueue = robotQueue
            self.setDataQueue = setDataQueue
            self.cmdDataQueue = cmdDataQueue
            self.serialParentPipev = serialParentPipe
            self.joyParentPipe = joyParentPipe
            self.hCamQueue = hCamQueue
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
        robotData = rasp_atmega.responseGetData
        return robotData

    def getEdge(self, frame):
        height, width = frame.shape[:2] # 이미지 높이, 너비
        
        gray_img = Edge.grayscale(frame) # 흑백이미지로 변환
            
        blur_img = Edge.gaussian_blur(gray_img, 3) # Blur 효과
        
        canny_img = Edge.canny(blur_img, 70, 210) # Canny edge 알고리즘
        
        vertices = np.array([[(150,height),(width/2-150, height/2+60), (width/2+150, height/2+60), (width-150,height)]], dtype=np.int32)
        ROI_img = Edge.region_of_interest(canny_img, vertices) # ROI 설정
        
        line_arr = Edge.hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) # 허프 변환
        line_arr = np.squeeze(line_arr)
            
        # 기울기 구하기
        slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi
        
        # 수평 기울기 제한
        line_arr = line_arr[np.abs(slope_degree)<160]
        slope_degree = slope_degree[np.abs(slope_degree)<160]
        # 수직 기울기 제한
        line_arr = line_arr[np.abs(slope_degree)>95]
        slope_degree = slope_degree[np.abs(slope_degree)>95]
        # 필터링된 직선 버리기
        L_lines, R_lines = line_arr[(slope_degree>0),:], line_arr[(slope_degree<0),:]
        temp = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
        L_lines, R_lines = L_lines[:,None], R_lines[:,None]
        # 왼쪽, 오른쪽 각각 대표선 구하기
        left_fit_line = Edge.get_fitline(frame,L_lines)
        right_fit_line = Edge.get_fitline(frame,R_lines)
        # 대표선 그리기vvv         
        Edge.draw_fit_line(temp, left_fit_line)
        Edge.draw_fit_line(temp, right_fit_line)
        # 방향을 찾기위한 소실점 구하기
        left_fit_line, left_x = Edge.get_point(frame,L_lines)
        right_fit_line, right_x = Edge.get_point(frame,R_lines)
        
        
        _point = (left_x + right_x) /2
        _center = frame.shape[1]/2
        
        direction = "None"
        if _center-3 >= _point and _center+3 <= _point:
            direction = "Go"
        elif _center > _point:
            direction = "Left"
        elif _center < _point:
            direction = "Right"
        
        red_color = (0, 0, 255)
        green_color = (0, 255, 0)
        
        temp = cv2.line(temp, (int(_point-5), 290), (int(_point-5), 290), red_color, 10)
        temp = cv2.line(temp, (int(_center-5), 290), (int(_center-5), 290), green_color, 10)
        
        cv2.putText(temp, str(direction), (30,50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        
        #print(left_fit_line)
        #print(right_fit_line)
        #print(image_w)
        result = Edge.weighted_img(temp, frame) # 원본 이미지에 검출된 선 overlap

        return result
    
    def realTimeStatusThread(self,id, ser_socket):
        comparativeData = self.comparative
        prev_time = time.time()
        fps = 10

        while True:
            
            cam = cv2.VideoCapture(2)
            #cam.set(3,320)
            #cam.set(4,240)
            while cam.isOpened():
                
                try:
                    ret, frame = cam.read()
                    current_time = time.time() - prev_time
                    if ret and (current_time > 1./fps):
                        prev_time = time.time()
                        if robotQueue.qsize() != 0:
                            robotData = robotQueue.get()
                            if comparativeData != robotData:
                                comparativeData = robotData
                        elif robotQueue.qsize() == 0:
                            robotData = comparativeData
                        
                        frame = cv2.flip(frame, 0)
                        frame = cv2.flip(frame, 1)
                        print("com1")
                        #frame = self.getEdge(frame)
                        print("com2")

                        result, frame = cv2.imencode('.jpg', frame, self.encode_param)
                        imgData = np.array(frame)
                        byteData = imgData.tobytes()
                        base64Data = self.byteTransformBase64(byteData)
                        realTimeData = robotData
                        
                        if realTimeData.get("type")!=None and realTimeData["type"] == "responseData":
                            del(realTimeData["type"])
                        
                        realTimeData["img"] = base64Data
                        if hCamQueue.qsize() != 0 :
                            realTimeData["img2"] = hCamQueue.get()
                        
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
                    print("err1:",e)
                    
                
            
    
    def transferData(self, ser_socket):
        self.connectionCheck(ser_socket)
        print("cli conn ok")

        while True:

            if self.robotQueue.qsize() != 0:
                robotData = robotQueue.get()
                self.comparative = robotData    
                if robotData["type"] == "responseData":
                    del(robotData["type"])
                    print(robotData)
                    break
        print("1Round")
        rsCheck = True
        while rsCheck:
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
        print("2Round")

        

        threadSend = Threading.Thread(target=self.realTimeStatusThread, args=(1, ser_socket))
        threadSend.start()
        print("3Round")
        while True:
            
            pass
            #getData = self.recvMSG(ser_socket)
            """getData = ""
            if(getData["type"] == "request/RobotSettingModify" and getData["origin"] == "aiServer"):
                pass
            elif(getData["type"] == "request/RobotControll" and getData["origin"] == "aiServer"):
                pass
            else: 
                pass"""

    def clientON(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((self.serverIP, self.serverPORT))
            print("gogo")
            self.transferData(sock)


while True:
    try:
        joycontroller = Joycon.joyCon()
        blueQueue = Queue()
        joyParentPipe, joyChildPipe = Pipe()
        joycon_MultiProcess = Process(target=joycontroller.joyControll, args=(blueQueue, joyChildPipe))


        rasp_atmega = raspAtmegaSerial.RaspAtmega()
        rasp_atmega.serialON()
        robotQueue = Queue()
        setDataQueue = Queue()
        cmdDataQueue = Queue()
        hCamQueue = Queue()
        
        serialParentPipe, serialChildPipe = Pipe()
        rasp_atmega_MultiProcess = Process(target=rasp_atmega.multipleStart, args=(robotQueue,setDataQueue,cmdDataQueue,blueQueue,serialChildPipe))
        
        humanCam = HumanCam.camera()
        hCam_MultiProcess = Process(target = humanCam.frameUpdate, args=(hCamQueue,))

        hCam_MultiProcess.start()
        rasp_atmega_MultiProcess.start()
        #joycon_MultiProcess.start()

        raspCLI_aiSER = SocketClient(robotQueue,setDataQueue,cmdDataQueue,serialParentPipe,hCamQueue,joyParentPipe)
        raspCLI_aiSER.clientON()
    except Exception as ex:
        print("err2:",ex)
