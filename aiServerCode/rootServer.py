import socket
import numpy as np
import cv2
import threading as Threading
from multiprocessing import Process, Queue
import millis
import json
import base64
import cvlib as cv
import numpy as np
import edge as Edge
import dbConnection as DataBase
import amg8833Edge
import imgSave
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


class SocketServer(object):
    __socket = ""
    __socketList = []
    __socketNames = []
    __robotData = {}
    __messageForm = {"origin":"aiServer",
                   "destination":"",
                   "type":"request/purpose",
                   "data":""}
    raspSocket = None
    webSocket = None
    
    __roadData = ""
    __faceData = ""
    __prevSaveTime = 0
    __warning = 0;

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, fileDictQueue):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            self.__socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.__socket.bind(("",8485))
            self.__socket.listen(5)
            self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            self.memberModel = load_model("model_rgb.h5")
            self.maskModel = load_model('mask_detector.model')
            self.testModel()
            self.fileDictQueue = fileDictQueue;
            cls._init = True
    
    
    def testModel(self):

        # # 사진 속에서 얼굴을 탐지하는 face_detector 모델
        # # 얼굴인식 후 마스크 착용 여부를 확인하는 모델
        

        img = cv2.imread("D:/project2021/Members/TestDataSet/TestDataSet/SeoTaeWoong/SeoTaeWoong (1).jpg");

        face_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_input = cv2.resize(face_input, dsize=(224, 224))
        face_input = preprocess_input(face_input)
        face_input = np.expand_dims(face_input, axis=0)

        (mask, nomask) = self.maskModel.predict(face_input)[0]
        
        img_size = (128,128)
        frame_resized = cv2.resize(img, img_size, interpolation=cv2.INTER_AREA) 
        frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

        frame_reshaped = frame_normalized.reshape((1, 128, 128,3))
        preprocessed = frame_reshaped
        prediction = self.memberModel.predict(preprocessed)
        
        print("complate")
    
    def getEdge(self, cli_socket, addr, roadFrame):
        try:
            frame = roadFrame
            
            height, width = frame.shape[:2] # 이미지 높이, 너비
            
            gray_img = Edge.grayscale(frame) # 흑백이미지로 변환
            
            blur_img = Edge.gaussian_blur(gray_img, 3) # Blur 효과
            
            canny_img = Edge.canny(blur_img, 70, 210) # Canny edge 알고리즘
            
            vertices = np.array([[(10,height),(width/2-120, height/2+20), (width/2+120, height/2+20), (width-10,height)]], dtype=np.int32)
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
            
            
            if self.__robotData["controll"] == 1:
                direction = "done"
                if _center-30 <= _point and _center+30 >= _point:
                    direction = "forward"
                elif _center-60 > _point:
                    direction = "left3"
                elif _center+60 < _point:
                    direction = "right3"
                elif _center-50 > _point:
                    direction = "left2"
                elif _center+50 < _point:
                    direction = "right2"
                elif _center-30 > _point:
                    direction = "left1"
                elif _center+30 < _point:
                    direction = "right1"
                else:
                    direction = "done"
                    
                message = self.__messageForm
                message["destination"] = addr[0]
                message["type"] = "request/RobotControll"
                message["data"] = direction
                self.sendMSG(cli_socket, message)
            
            red_color = (0, 0, 255)
            green_color = (0, 255, 0)
            blue_color = (255, 0, 0)
            
            black_color = (127,128,127)
            
            temp = cv2.line(temp, (int(_point-5), 100), (int(_point-5), 100), red_color, 10)
            
            temp = cv2.line(temp, (int(_center-2), 100), (int(_center-2), 100), blue_color, 4)
            
            temp = cv2.line(temp, (int(_center-10), 95), (int(_center-10), 105), green_color, 4)
            temp = cv2.line(temp, (int(_center+10), 95), (int(_center+10), 105), green_color, 4)
            
            temp = cv2.line(temp, (int(_center-30), 95), (int(_center-30), 105), black_color, 4) #Left1
            temp = cv2.line(temp, (int(_center+30), 95), (int(_center+30), 105), black_color, 4) #Right1
            
            temp = cv2.line(temp, (int(_center-60), 95), (int(_center-60), 105), green_color, 4) #Left2
            temp = cv2.line(temp, (int(_center+60), 95), (int(_center+60), 105), green_color, 4) #Right2
            
            temp = cv2.line(temp, (int(_center+90), 95), (int(_center+90), 105), black_color, 4) #Right3
            temp = cv2.line(temp, (int(_center-90), 95), (int(_center-90), 105), black_color, 4) #Left3

            
    
            cv2.putText(temp, str(direction), (30,50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
            
            #print(left_fit_line)
            #print(right_fit_line)
            #print(image_w)
            result = Edge.weighted_img(temp, frame) # 원본 이미지에 검출된 선 overlap
            
            self.__roadData = result
            
        except Exception as e:
            self.__roadData = roadFrame
            if self.__robotData["controll"] == 1:
                message = self.__messageForm
                message["destination"] = addr[0]
                message["type"] = "request/RobotControll"
                message["data"] = "done"
                self.sendMSG(cli_socket, message)
            
            
            

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
    
    def byteTransformBase64(self, frame):
        encoded = base64.b64encode(frame)
        return encoded.decode("ascii")
    
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
                        if getData["origin"] == "rasp":
                            self.raspSocket = cli_socket
                            return
                        elif getData["origin"] == "web":
                            self.webSocket = cli_socket
                            return
    
    
    
    def transferData(self, cli_socket, addr):
        self.connectionCheck(cli_socket, addr)
        noneIMG = cv2.imread("noneIMG.jpg")
        result, noneIMG = cv2.imencode('.jpg', noneIMG, self.encode_param)
        noneIMG = np.array(noneIMG)
        noneIMG = noneIMG.tobytes()
        noneImgBase64Data = self.byteTransformBase64(noneIMG)
        
        while True:
            getData = self.recvMSG(cli_socket, addr)
            
            if(getData and getData["type"] == "request/RobotSettings" and getData["origin"] == "rasp"):
                print("작동")    
                message = self.__messageForm
                message["destination"] = addr[0]
                message["type"] = "response/RobotSettings"
                message["data"] = "ok"
                self.sendMSG(cli_socket, message)
                print("robotSettings 응답 완료")
                print("받은 데이터 ", getData)
                self.__robotData = getData["data"]
                #여기서 웹으로 데이터 전송 코드 작성하기
                #
                #
                
            elif(getData and getData["type"] == "request/RealTimeStatus" and getData["origin"] == "rasp"):
                
                try:
                    if getData["data"]["humanData"] == "NoneImg":
                        humanData = noneImgBase64Data
                    else:
                        humanData = getData["data"]["humanData"]["img"] 
                        amg8833Data = getData["data"]["humanData"]["amg8833"]
                        
                        timeData = getData["data"]["humanData"]["time"] 
                        self.humanData={"amg8833": amg8833Data, "time":timeData}
                    roadData = getData["data"]["roadData"]["img"]
                    
                    # for key,value in getData["data"].items():
                    #     if key != "humanData" and key != "roadData":
                    #         print(key, value)
                    # print(getData["data"]["humanData"]["amg8833"])
                    # print(getData["data"]["humanData"]["time"])
                    
                    roadCam = self.base64TransformImg(roadData)
                    humanCam = self.base64TransformImg(humanData)
                    roadCamData = np.frombuffer(roadCam, dtype = 'uint8')
                    humanCamData = np.frombuffer(humanCam, dtype = 'uint8')
                    #data를 디코딩한다.
                    roadCam = cv2.imdecode(roadCamData, cv2.IMREAD_COLOR)
                    humanCam = cv2.imdecode(humanCamData, cv2.IMREAD_COLOR)
                    
                    roadThread = Threading.Thread(target=self.getEdge, args=(cli_socket, addr, roadCam))
                    roadThread.daemon=True
                    roadThread.start()

                    faceThread = Threading.Thread(target=self.faceEdge, args=(humanCam,))                    
                    faceThread.daemon = True
                    faceThread.start()
                    
                    
                    
                    roadThread.join()
                    faceThread.join()

                    roadEdgeData = self.__roadData
                    faceEdgeData = self.__faceData
                    

                    try:
                        cv2.imshow("roadCam",roadEdgeData)
                        cv2.imshow("humanCam",faceEdgeData)
                        #cv2.imshow("roadCam",roadCam)
                        #cv2.imshow("humanCam",humanCam)
                        cv2.waitKey(1)
                    except :
                        pass
                    
                       
                            
                    if self.webSocket != None:
                        
                        # result, roadCam = cv2.imencode('.jpg', roadEdgeDatas, self.encode_param)
                        # raodCamData = np.array(roadCam)
                        # roadCamByteData = raodCamData.tobytes()
                        # roadCamBase64Data = self.byteTransformBase64(roadCamByteData)
                        
                        result, humanCam = cv2.imencode('.jpg', faceEdgeData, self.encode_param)
                        humanCamData = np.array(humanCam)
                        humanCamByteData = humanCamData.tobytes()
                        humanCamBase64Data = self.byteTransformBase64(humanCamByteData)
                        
                        data = {"roadCam": roadData ,"humanCam": humanCamBase64Data,"warning": self.__warning}
                        message = self.__messageForm
                        message["destination"] = "web"
                        message["type"] = "request/RealTimeStatus"
                        message["data"] = data
                        self.sendMSG(self.webSocket,message)
                        
                        self.__warning = 0;
                except Exception as e:
                    pass
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
               
    def faceEdge(self, imgFrame):
        try:
            faces, confidences = cv.detect_face(imgFrame)
            
            for (x, y, x2, y2), conf in zip(faces, confidences):
                
                img_size = (128,128)
                #img = gray[y-20:y2+20,x-20:x2+20].copy()
                #grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #rgbImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2RGB)
                #frame_resized = cv2.resize(rgbImg, img_size, interpolation=cv2.INTER_AREA) 
                img = imgFrame[y-20:y2+20,x-20:x2+20].copy()
                frame_resized = cv2.resize(img, img_size, interpolation=cv2.INTER_AREA) 
                frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    
                frame_reshaped = frame_normalized.reshape((1, 128, 128,3))
                preprocessed = frame_reshaped
                prediction = self.memberModel.predict(preprocessed)
                
                pred = np.argmax(np.squeeze(prediction))
                name = "Unknown"
                if(prediction[0][pred] > 0.9):
                    if(pred == 0):
                        name = "JangYungDae"
                    elif(pred == 1):
                        name = "KimSungTan"
                    elif(pred == 2):
                        name = "SeoTaeWoong"
                        
                maskStatus = 0        
                age = "Unknown"
                gender = 2
                face_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                face_input = cv2.resize(face_input, dsize=(224, 224))
                face_input = preprocess_input(face_input)
                face_input = np.expand_dims(face_input, axis=0)
                (mask, nomask) = self.maskModel.predict(face_input)[0]
                if mask > nomask:
                    maskStatus = 0
                else:
                    maskStatus = 1
                    gender, age = self.getGender_Age(img)
                    
                
                
                currentSaveTime = millis.Millis() - self.__prevSaveTime
                if currentSaveTime > 2000 :
                    self.__prevSaveTime = millis.Millis()
                    # 전송할 데이터 : 사람 img , 온도 img , 찍힌시간, 8*8온도 데이터
                    filePath = "D:/project2021/imgFileServer/"
                    shootingTime = str(self.humanData["time"])
                    
                    #디렉터리생성
                    directoryNameList = shootingTime.replace(' ', '/').split('/')
                    
                    imgSave.createDirectory(directoryNameList, filePath)
                    
                    path = filePath+directoryNameList[0]+"/"+directoryNameList[1]+"/"+directoryNameList[2]+"/"+directoryNameList[3]
                    #이미지 저장
                    imgPath1 = path+"/fullImg.jpg"
                    cv2.imwrite(imgPath1, imgFrame)
                    imgPath2 = path+"/humanImg.jpg"
                    cv2.imwrite(imgPath2, img)
                    amgPath = path+"/amg8833.jpg"
                    amgData = self.humanData["amg8833"]
                    datashape = np.reshape(amgData,(8,8))
                    dataflip = np.flip(datashape, axis=1)
                    
                    print("1")
                    h, w, c = imgFrame.shape
                    wRatio48 = round(w/48.0)
                    hRatio48 = round(h/48.0)
                    amgRectPath = path+"/amg8833Rect.jpg"
                    print("2")
                    _amgLocationX1 = int(round((x-10)/wRatio48,0))
                    _amgLocationY1 = int(round((y-10)/hRatio48,0))
                    
                    _amgLocationX2 = int(round((x2+10)/wRatio48,0))
                    _amgLocationY2 = int(round((y2+10)/hRatio48,0))
                    print("3")
                    imgSave.amg8833_IMG_Save(dataflip, amgPath, amgRectPath, _amgLocationX1, _amgLocationY1, _amgLocationX2, _amgLocationY2)                
                    print("4")
                    fileDict={"imgPath":imgPath1, "amgPath":amgRectPath}
                    self.fileDictQueue.put(fileDict)
                    
                    
                    
                    #온도 데이터
                    wRatio8 = round(w/8.0)
                    hRatio8 = round(h/8.0)
                    
                    amgLocationX1 = int(round((x-10)/wRatio8,0))
                    amgLocationY1 = int(round((y-10)/hRatio8,0))
                    
                    amgLocationX2 = int(round((x2+10)/wRatio8,0))
                    amgLocationY2 = int(round((y2+10)/hRatio8,0))
                    
                    _total = 0
                    
                    amgArray = dataflip
                    
                    for x in range(amgLocationX1, amgLocationX2):
                        for y in range(amgLocationY1, amgLocationY2):
                            _total += amgArray[x][y]
                    
                    _avr = round(_total/(len(range(amgLocationX1, amgLocationX2))*len(range(amgLocationY1, amgLocationY2))),1)
                    print(_avr)
                    mysqlDB = DataBase.MysqlConnector()
                    warning = 0;
                    if (_avr > 28) or (maskStatus == 1):
                        warning = 1
                    self.__warning = warning
                    detectUserDict = {
                            "temp" : _avr,
                            "mask" : maskStatus,
                            "name" : name,
                            "age" : age,
                            "gender" : gender,
                            "shootingDate" : shootingTime,
                            "checked" : 0,
                            "warning" : warning
                        }
                    
                    #mask값 gender값 age값 유동적 구하는 model 찾
                    imgPathDict = {
                            "dutseq" : 0,
                            "original_imgpath" : imgPath1,
                            "original_ir_imgpath" : amgPath,
                            "detail_imgpath" : imgPath2,
                            "detail_ir_imgpath" : amgRectPath
                            }
                    
                    
                    dbThread = Threading.Thread(target=mysqlDB.insertData, args=(detectUserDict , imgPathDict))
                    dbThread.daemon = True
                    dbThread.start()
                    
                    
                
                
                if maskStatus == 0:
                    textColor = (0,255,0)
                else:
                    textColor = (0, 0, 255)
                cv2.rectangle(imgFrame, (x-20, y-20), (x2+20, y2+20), textColor, 2)
                cv2.putText(imgFrame, str(name), (x+30,y-40), cv2.FONT_HERSHEY_PLAIN, 1, textColor, 2)
                
                if "dbThread" in locals():
                    dbThread.join()
                
            self.__faceData = imgFrame
            return
        except Exception as e:
            if "dbThread" in locals():
                dbThread.join()
            self.__faceData = imgFrame
            print(e)
            return
    
    def getGender_Age(self, img):
        MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        age_net = cv2.dnn.readNetFromCaffe(
        	'deploy_age.prototxt',
        	'age_net.caffemodel')

        # 성별 예측 모델 불러오기
        gender_net = cv2.dnn.readNetFromCaffe(
        	'deploy_gender.prototxt',
        	'gender_net.caffemodel')

        # 연령 클래스
        age_list = ['(0 ~ 2)','(4 ~ 6)','(8 ~ 12)','(15 ~ 20)',
                    '(25 ~ 32)','(38 ~ 43)','(48 ~ 53)','(60 ~ 100)']
        # 성별 클래스
        gender_list = ['0', '1']
        blob = cv2.dnn.blobFromImage(img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            
        # gender detection
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        # 가장 높은 Score값을 선정
        gender = gender_preds.argmax()
        # Predict age
        age_net.setInput(blob)
        age_preds = age_net.forward()
        # 가장 높은 Score값을 선정
        age = age_preds.argmax()

        return gender_list[gender], age_list[age]
                
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
                tData.daemon = True
                tData.start()
            except KeyboardInterrupt:
                self.__socket.close()
                print("Keyboard interrupt")
            
            


if __name__ == "__main__":
    fileDictQueue = Queue()
    amgEdge = amg8833Edge.amg8833()
    amgEdgeProcess = Process(target=amgEdge.createAmg8833Edge, args=(fileDictQueue,))
    amgEdgeProcess.daemon = True
    amgEdgeProcess.start()
    
    a = SocketServer(fileDictQueue)
    a.serverON()
    