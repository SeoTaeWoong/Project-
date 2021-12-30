
def strAsDictFormat(str):
    dictResult = {}
    key = []
    value = []
    str = str[1:len(str)-1]
    strSpList = str.split(",")
    cnt = 0
    tmp = ""
    for _str in strSpList:
        _strSpList = _str.split(":")
        
        for __str in _strSpList:
            t
            if cnt==0:
                key.append(__str)
                cnt+=1
            elif cnt==1:
                tmp += __str
                if tmp[:1] == "{":
                    if tmp[-1:] == "}":
                        value.append(tmp)
                        tmp=""
                        cnt-=1
                else:
                    value.append(tmp)
                    tmp=""
                    cnt-=1
        
    print(key,value)
    return


test = '{"Connection":{"mode":"Web","Kp":1},"id":"keroro"}'
strAsDictFormat(test)
