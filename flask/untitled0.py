import time
from multiprocessing import Process, Queue, Array

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
            
    def test1(self,id,start,end,result,testQ, tempC):
        total = 0
        
        
                
        for i in range(start,end):
            total+=i
        result.put(total)
        return
    

class tempClass():
    a=5

if __name__ == "__main__":
    k=3
    testC = testClass()
    tempC = tempClass()
    start_time = time.time()
    START, END = 0, 100000000
    result = Queue()
    testQ = Queue()
    
    th1 = Process(target=testC.test1, args=(1, START, END//2, result, testQ, tempC))
    th2 = Process(target=testC.test1, args=(2, END//2, END, result, testQ, tempC))
    
    testC.z = 15
    
    tempC.a = 12
    
    th1.start()
    th2.start()
    
    tempC.a = 15
    
    th1.join()
    th2.join()
    
    result.put('STOP')
    
    total = 0
    while True:
        tmp = result.get()
        if tmp == 'STOP':
            break
        else:
            total += tmp
    print(f"Result: {total}")
    
    end_time = time.time()
    print(f"total elapsed time : {end_time - start_time}")
    
    di = {"aa":"1","bb":2}
    
    
        
