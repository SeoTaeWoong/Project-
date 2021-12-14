import struct
import serial

ser = serial.Serial('/dev/ttyAMA2', 115200, timeout = 0.005)

jsdev = open("/dev/input/js0","rb")

button = {
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

stick = {
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

type_0x01_cnt = 0
type_0x02_cnt = 0
getKey = ""
while True:
    
    evbuf = jsdev.read(8)
    

    if evbuf:
        _time, _value, _type, _number = struct.unpack("IhBB",evbuf)
        if _type & 0x01:
            if type_0x01_cnt < 16:
                type_0x01_cnt+=1
            else:
                #print(button[_number])
                getKey = button[_number]
                encoded = (getKey+'\0').encode('utf-8')
                ser.write(encoded)
                print(ser.readline().decode('euc-kr'))
        if _type & 0x02:
            if type_0x02_cnt < 6:
                type_0x02_cnt+=1
            else:
                #print(stick[_number][_value])
                getKey = stick[_number][_value]
                encoded = (getKey+'\0').encode('utf-8')
                ser.write(encoded)
                print(ser.readline().decode('euc-kr'))
