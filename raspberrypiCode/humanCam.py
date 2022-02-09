import cv2
import socket
import numpy as np
import time
import base64
import threading as Threading
from queue import Queue
import amg8833_i2c




class camera(object):
    index = 0
    camThread = {}
    realCam = None
    frames = {}
    status = {}
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            cls._init = True
            
    
    def amg8833Start(self):
        while True:
            t0 = time.time()
            self.sensor = []
            while (time.time()-t0)<1: # wait 1sec for sensor to start
                try:
                    self.sensor = amg8833_i2c.AMG8833(addr=0x69) # start AMG8833
                except:
                    self.sensor = amg8833_i2c.AMG8833(addr=0x68)
                finally:
                    pass
            time.sleep(0.1) # wait for sensor to settle
            # If no device is found, exit the script
            if self.sensor==[]:
                print("No AMG8833 Found - Check Your Wiring")
                continue
            else:
                print("AMG8833 OK")
                return
    
    def getAMG8833(self, amgDataQue):
        pix_to_read = 64
        while True:
            status,data = self.sensor.read_temp(pix_to_read) # read pixels with status
            
            if status:
                continue
            else:
            
                amgDataQue.put(data)
                return 


    def byteTransformBase64(self, frame):
        encoded = base64.b64encode(frame)
        return encoded.decode("ascii")
    

    
    def checkCam(self):
        i=-1
        while i<2:
            cam = cv2.VideoCapture(i)
            cam.set(3,320)
            cam.set(4,240)
            if cam.isOpened():
                self.realCam = cam
                self.index+=1
                print("check OK,  openCam :", self.index)
                return self.index
            else:
                cam.release()
            i+=1
        
        return self.index
    
    def frameUpdate(self, hCamQueue, amg8833Queue, hCamTimeQueue):
        print("update~~")
        prev_time = time.time()
        fps = 10
        self.amg8833Start()
        
        while True:
            index = self.checkCam()
            
            if index == 1:
                while self.realCam.isOpened():
                    try:
                        ret, frame = self.realCam.read()
                        current_time = time.time() - prev_time
                        if ret and current_time > 1./fps:
                            prev_time = time.time()
                            amgDataQue = Queue()
                            amg8833Thread = Threading.Thread(target=self.getAMG8833, args=(amgDataQue,))
                            amg8833Thread.start()
                            frame = cv2.flip(frame,1)
                            frame = cv2.flip(frame,0)
                            result, frame = cv2.imencode('.jpg', frame, self.encode_param)
                            imgData = np.array(frame)
                            byteData = imgData.tobytes()
                            base64Data = self.byteTransformBase64(byteData)
                            
                            now = time.localtime()
                            imgTime = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                            
                            amg8833Thread.join()
                            
                            if hCamQueue.qsize() > 20:
                                hCamQueue.get()
                                amg8833Queue.get()
                                hCamTimeQueue.get()
                                
                                hCamQueue.put(base64Data)
                                amg8833Queue.put(amgDataQue.get())
                                hCamTimeQueue.put(imgTime)
                            else:
                                hCamQueue.put(base64Data)
                                amg8833Queue.put(amgDataQue.get())
                                hCamTimeQueue.put(imgTime)
                                
                            
                    except Exception as e:
                        self.realCam.release()
                        cv2.destroyAllWindows()
                        print("humanCam err1:",e)
        

    def showFrame(self):
        cv2.imshow("test1", self.frames[0])
        cv2.imshow("test2", self.frames[1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.realCam[0].release()
            self.realCam[1].release()
            cv2.destroyAllWindows()
            
       