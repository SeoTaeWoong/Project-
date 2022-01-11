import time

def Millis():
    millis = int(round(time.time()*1000))
    return millis

str1 = "type:ply,data:10,minSPD:20"

a = {}

a[0]= {"a":"b","c":"d"}
a[1]= {"a":"b","c":"d"}

print(a)
if "type:" in str1:
    print("true")

print(str1)
dict = {}
str2 = str1.split(",")
i = 0
for key in str2:
    item = key.split(":")
    dict[item[0]] = item[1]
    
del(dict["type"])
for key,value in dict.items():
    if key != "data":
        print(value)
    



