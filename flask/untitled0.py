import time
from multiprocessing import Process, Queue, Array
import threading as Threading

class testClass():
    z = 2
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            cls._init = True
            
    def test1(self):
        
        _i = 0
        
        while True:
            _i+=1
            self.getData = _i
            time.sleep(0.1)
            
        
    

a = testClass()

aThread = Threading.Thread(target=a.test1, args=())
i = 0
aThread.start()
while(True):
    print("i :", i)
    print("aThread:", a.getData)
    i+=1
    time.sleep(0.1)
    