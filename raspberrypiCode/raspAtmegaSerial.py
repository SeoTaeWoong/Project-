import serial
import millis
import threading as Threading
import time

class RaspAtmega(object):
    __responseGetData={}
    __responseErrData={}
    controller = 1 # 0 : AUTO, 1: JOYCON, 2:WEB
    maxSPD = 0
    minSPD = 0
    kp = 0
    ki = 0
    kd = 0

    types=[True,False,False]

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            self.serialPort = '/dev/ttyAMA2'
            self.baudRate = 115200
            self.timeout = 0.001
            cls._init = True
    
    def serialON(self):
        self.ser = serial.Serial(self.serialPort, self.baudRate, timeout = self.timeout)
    
    def setData(self,controller, maxSPD, minSPD, kp, ki,kd):
        self.controller = controller
        self.maxSPD = maxSPD
        self.minSPD = minSPD
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def setCMD(self, cmd):
        self.cmd = cmd

    def dataTransformByteLength(self, data):
        return str(len(data)).encode().ljust(16)

    def getRobotData(self):
        return self.__responseGetData

    def getDataTransmit(self, lock):
        while True:
            if self.types[0]:
                with lock:
                    self.serialWrite("getData")
                    time.sleep(0.2)

    def setDataTransmit(self, lock):
        while True:
            if self.types[1]:
                with lock:
                    self.serialWrite("setData")
                    time.sleep(0.2)
                    self.types[1] = False

    def cmdDataTransmit(self, lock):
        while True:
            if self.types[2]:
                with lock:
                    self.serialWrite("command")
                    time.sleep(0.2)
                    self.types[2] = False

    def serialWrite(self, type):
        # 스레드 동기화 필요 
        # 동시에 해당 함수를 실행시에 에러발생확률 증가
        _action = True
        _timeOut = millis.Millis()
        if type == "getData":
            #응답 데이터 없으면 재전송
            while _action:
                msg = "type:getData,0\0"
                encoded = msg.encode('utf-8')
                self.ser.write(encoded)
                startTime = millis.Millis()
                while _action:
                    data = self.ser.readline()
                    data = data.decode("utf-8")
                    endTime = millis.Millis()
                    if "type:responseData" in data:
                        print(data,"read---OK")
                        items = data.split(",")
                        self.__responseGetData = {}
                        for item in items:
                            _item = item.split(":")
                            try:
                                self.__responseGetData[_item[0]] = _item[1]
                            except:
                                pass
                        return
                    elif (endTime-startTime) > 300:
                        break
                if (endTime-_timeOut) > 1000 and _action:
                    self.__responseErrData[0] = {"type":"errMSG","data":"getData TimeOUT","time":str((endTime-_timeOut)/1000)+"s"}
                    print(data,"---err")
                    break
            
        elif type == "setData":
            #응답 데이터 없으면 재전송
            while _action:
                msg = "type:setData,controller:"+str(self.controller)+"maxSPD:"+str(self.maxSPD)+",minSPD:"+str(self.minSPD)+",Kp:"+str(self.kp)+",Ki:"+str(self.ki)+",Kd:"+str(self.kd)+'\0'
                encoded = msg.encode('utf-8')
                self.ser.write(encoded)
                startTime = millis.Millis()
                while _action:
                    data = self.ser.readline()
                    data = data.decode("utf-8")
                    endTime = millis.Millis()
                    if "dataSettings:Ok" in data:
                        print(data)
                        _action = False
                    elif (endTime-startTime) > 300:
                        break
                if (endTime-_timeOut) > 1000 and _action:
                    self.__responseErrData[1] = {"type":"errMSG","data":"setData TimeOUT","time":str((endTime-_timeOut)/1000)+"s"}
                    print(data,"---err")
                    break

        elif type == "command":
            #응답 데이터 없으면 재전송
            while _action:
                msg = "type:command, controll:"+str(self.cmd)+'\0'
                encoded = msg.encode('utf-8')
                self.ser.write(encoded)
                startTime = millis.Millis()
                while _action:
                    data = self.ser.readline()
                    data = data.decode("utf-8")
                    endTime = millis.Millis()
                    if "motorControll:Ok" in data:
                        print(data)
                        _action = False
                    elif (endTime-startTime) > 300:
                        break
                if (endTime-_timeOut) > 1000 and _action:
                    self.__responseErrData[2] = {"type":"errMSG","data":"motorControll TimeOUT","time":str((endTime-_timeOut)/1000)+"s"}
                    print(data,"---err")
                    break

            pass
        else:
            pass


a = RaspAtmega()
a.serialON()    
rasp_atmega_getDataT = Threading.Thread(target=a.getDataTransmit, args=(Threading.Lock(),))
rasp_atmega_getDataT.start()