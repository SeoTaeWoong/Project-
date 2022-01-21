import cv2
import socket
import numpy as np
import time
import base64



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

    def byteTransformBase64(self, frame):
        encoded = base64.b64encode(frame)
        return encoded.decode("ascii")
    
    def checkCam(self):
        i=-1
        while i<2:
            cam = cv2.VideoCapture(i)
            if cam.isOpened():
                self.realCam = cam
                self.index+=1
                print("check OK,  openCam :", self.index)
                return self.index
            else:
                cam.release()
            i+=1
        
        return self.index
    
    def frameUpdate(self, hCamQueue):
        print("update~~")
        prev_time = time.time()
        fps = 10

        while True:
            index = self.checkCam()
            if index == 1:
                while self.realCam.isOpened():
                    try:
                        ret, frame = self.realCam.read()
                        current_time = time.time() - prev_time
                        if ret and current_time > 1./fps:
                            result, frame = cv2.imencode('.jpg', frame, self.encode_param)
                            imgData = np.array(frame)
                            byteData = imgData.tobytes()
                            base64Data = self.byteTransformBase64(byteData)
                            if hCamQueue.qsize() > 20:
                                hCamQueue.get()
                                hCamQueue.put(base64Data)
                            else:
                                hCamQueue.put(base64Data)
                            prev_time = time.time()
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
            
       