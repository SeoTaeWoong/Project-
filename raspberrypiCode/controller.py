import struct
 
class joyCon:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            self.button = {
                    0:"A_key",
                    1:"X_key",
                    2:"B_key",
                    3:"Y_key",
                    4:"SL_key",
                    5:"SR_key",
                    12:"HOME_key",
                    14:"R_key",
                    15:"ZR_key"
            }
            self.stick = {
            4 : {
                -32767 : "backward",
                32767 : "forward",
                0 : "done"
                },
            5 : {
                -32767 : "leftTurn",
                32767 : "rightTurn",
                0 : "done"
                }   
            }
            cls._init = True
            
    def joyControll(self,blueQueue,joyChildPipe):
        type_0x01_cnt = 0
        type_0x02_cnt = 0
        getKey = ""
        tempKey = ""
        
        while True:
            print("~~")
            try:
                jsdev = open("/dev/input/js0","rb")
                while True:
                    evbuf = jsdev.read(8)
                    if evbuf:
                        _time, _value, _type, _number = struct.unpack("IhBB",evbuf)
                        if _type & 0x01:
                            if type_0x01_cnt < 16:
                                type_0x01_cnt+=1
                            else:
                                #print(button[_number])
                                getKey = self.button[_number]
                                print(getKey)
                                #return getKey
                        if _type & 0x02:
                            if type_0x02_cnt < 6:
                                type_0x02_cnt+=1
                            else:
                                #print(stick[_number][_value])
                                getKey = self.stick[_number][_value]
                                if(getKey != tempKey):
                                    print(getKey)
                                    blueQueue.put(getKey)
                                tempKey = getKey
                                
            except Exception as e:
                print("bluetooth pire error")
                print(e)
