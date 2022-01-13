import serial
import millis
import threading as Threading
import time
import controller as joycon

class RaspAtmega(object):
              #controll 1 : AUTO, 2: JOYCON, 3:WEB
    __robotData={"controll":0,"maxSPD":0,"minSPD":0,"kp":0.0,"ki":0.0,"kd":0.0,}
    __responseErrData={}
    __command = ""
    

    types=[True,False,False]

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("rasp&atMEGA__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("rasp&atMEGA__init__\n")
            self.serialPort = '/dev/ttyAMA2'
            self.baudRate = 115200
            self.timeout = 0.001
            cls._init = True
    
    def serialON(self):
        self.ser = serial.Serial(self.serialPort, self.baudRate, timeout = self.timeout)
    
    def multipleStart(self, robotQueue,setDataqueue, cmdQueue, raspcliPipe):
        self.robotQueue = robotQueue
        self.raspcliPipe = raspcliPipe
        self.setDataQueue = setDataqueue
        self.cmdQueue = cmdQueue
        lock = Threading.Lock()
        getDataThread = Threading.Thread(target=self.getDataTransmit, args=(lock,))
        setDataThread = Threading.Thread(target=self.setDataTransmit, args=(lock,))
        cmdDataThread = Threading.Thread(target=self.cmdDataTransmit, args=(lock,))

        getDataThread.start()
        setDataThread.start()
        cmdDataThread.start()

        getDataThread.join()
        setDataThread.join()
        cmdDataThread.join()


    def setData(self,controller, maxSPD, minSPD, kp, ki,kd):
        self.__robotData["controll"] = controller
        self.__robotData["maxSPD"] = maxSPD
        self.__robotData["minSPD"] = minSPD
        self.__robotData["kp"] = kp
        self.__robotData["ki"] = ki
        self.__robotData["kd"] = kd

    def setCMD(self, cmd):
        self.__command = cmd

    def dataTransformByteLength(self, data):
        return str(len(data)).encode().ljust(16)

    def getRobotData(self):
        return self.__robotData

    def getDataTransmit(self, lock):
        while True:
            if self.types[0]:
                lock.acquire()
                self.serialWrite("getData")
                lock.release()
                time.sleep(0.5)
            

    def setDataTransmit(self, lock):
        while True:
            if self.types[1]:
                lock.acquire()
                self.serialWrite("setData")
                lock.release()
                time.sleep(0.2)
                self.types[1] = False

    def cmdDataTransmit(self, lock):
        
        while True:
            
            if self.types[2]:
                lock.acquire()
                self.serialWrite("controll")
                lock.release()
                time.sleep(0.2) 
                self.types[2] = False
            elif self.__robotData.get("controll") !=None and (self.__robotData["controll"] == 2) and (not self.types[2]):
                
                self.__command = joycon.joyControll()
                print(self.__command)
                if self.__command:
                    lock.acquire()
                    self.serialWrite("controll")
                    lock.release()
                    time.sleep(0.2)
         

    def serialWrite(self, type):
        # 스레드 동기화 필요 
        # 동시에 해당 함수를 실행시에 에러발생확률 증가
        _timeOut = millis.Millis()
        if type == "getData":
            #응답 데이터 없으면 재전송
            while True:
                msg = "type:getData,0\0"
                encoded = msg.encode('utf-8')
                self.ser.write(encoded)
                startTime = millis.Millis()
                while True:
                    data = self.ser.readline()
                    data = data.decode("utf-8")
                    endTime = millis.Millis()
                    if "type:responseData" in data:
                        items = data.split(",")
                        self.__robotData = {}
                        for item in items:
                            _item = item.split(":")
                            try:
                                if(_item[0] == "controll"):
                                    _item[1] = int(_item[1])
                                elif(_item[0] == "maxSPD"):
                                    _item[1] = int(_item[1])
                                elif(_item[0] == "minSPD"):
                                    _item[1] = int(_item[1])
                                elif(_item[0] == "kp"):
                                    _item[1] = float(_item[1])
                                elif(_item[0] == "ki"):
                                    _item[1] = float(_item[1])
                                elif(_item[0] == "kd"):
                                    _item[1] = float(_item[1])
                                
                                self.__robotData[_item[0]] = _item[1]
                            except:
                                pass
                            if(self.robotQueue.qsize() < 1):
                                self.robotQueue.put(self.__robotData)
                        return
                    elif (endTime-startTime) > 300:
                        break
                if (endTime-_timeOut) > 1000:
                    self.__responseErrData[0] = {"type":"errMSG","data":"getData TimeOUT","time":str((endTime-_timeOut)/1000)+"s"}
                    print(data,"---err")
                    break
            
        elif type == "setData":
            #응답 데이터 없으면 재전송
            while True:
                msg = "type:setData,"+str(self.__controller)+","+str(self.__maxSPD)+","+str(self.__minSPD)+","+str(self.__kp)+","+str(self.__ki)+","+str(self.__kd)+'\0'
                encoded = msg.encode('utf-8')
                self.ser.write(encoded)
                startTime = millis.Millis()
                while True:
                    data = self.ser.readline()
                    data = data.decode("utf-8")
                    endTime = millis.Millis()
                    if "dataSettings:ok" in data:
                        return
                    elif (endTime-startTime) > 300:
                        break
                if (endTime-_timeOut) > 1000:
                    self.__responseErrData[1] = {"type":"errMSG","data":"setData TimeOUT","time":str((endTime-_timeOut)/1000)+"s"}
                    print(data,"---err")
                    break

        elif type == "controll":
            #응답 데이터 없으면 재전송
            while True:
                msg = "type:controll,"+self.__command+'\0'
                encoded = msg.encode('utf-8')
                self.ser.write(encoded)
                print(msg)
                startTime = millis.Millis()
                while True:
                    data = self.ser.readline()
                    data = data.decode("utf-8")
                    endTime = millis.Millis()
                    if "motorControll:ok" in data:
                        return
                    elif (endTime-startTime) > 300:
                        break
                if (endTime-_timeOut) > 1000:
                    self.__responseErrData[2] = {"type":"errMSG","data":"motorControll TimeOUT","time":str((endTime-_timeOut)/1000)+"s"}
                    print(data,"---err")
                    break

            pass
        else:
            pass


#a = RaspAtmega()
#a.serialON()    
#rasp_atmega_getDataT = Threading.Thread(target=a.getDataTransmit, args=(Threading.Lock(),))
#rasp_atmega_getDataT.start()