import pymysql as db

class MysqlConnector(object):
    

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            self.__host = "121.139.165.163"
            self.__port = 8486
            self.__user = "admin"
            self.__passwd = "1q2w3e4r"
            self.__db = "teamproject"
            
            #self.__conn = db.connect(host="192.168.137.1", user="admin", passwd="1q2w3e4r", db= "teamproject", port=3306, use_unicode=True, charset='utf8')
            cls._init = True
    

    def getPageData(self, page, num):
        try:
            conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
            curs = conn.cursor()
            sql = "select count(*) from detectTB"
            curs.execute(sql)
            total = curs.fetchall()
            
            total = total[0][0]
            
            paging = int((total+num)/num)
            maxVal = page*num
            minVal = maxVal - num
            sql = "select * from detectTB order by seq desc limit %d,%d;"
            curs.execute(sql, minVal, maxVal)
            
            tupleData = curs.fetchall()
            curs.close()
            listData = list(tupleData)
            for index in range(len(listData)):
                listData[index] = list(listData[index])
                listData[index][2] = listData[index][2].replace("D:/project2021/imgFileServer/","mntimg/")
                listData[index][3] = listData[index][3].replace("D:/project2021/imgFileServer/","mntimg/")
                listData[index][4] = listData[index][4].replace("D:/project2021/imgFileServer/","mntimg/")
                listData[index][5] = listData[index][5].replace("D:/project2021/imgFileServer/","mntimg/")
                listData[index] = tuple(listData[index])
            tupleData = tuple(listData)
            conn.close()
            return tupleData, paging
        except Exception as e:
            print(e)
      
    def getDetectUser(self):
        try:
 
            conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
            curs = conn.cursor()
            sql = "select * from detectUserTB where warning = 1 and memberEmail is null  order by seq desc;"
            curs.execute(sql)
            tupleData = curs.fetchall()
            curs.close()
            conn.close()
            return tupleData
        except Exception as e:
            print("err1",e)
            
    def getInfoData(self, seq):
        try:
            conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
            curs = conn.cursor()
            sql = "update detectUserTB set checked = 1 where seq = %s";
            curs.execute(sql, (seq))
            conn.commit()
            
            sql = "select d.seq, d.name,d.age, d.gender, d.temp, d.mask, p.original_imgpath, p.original_ir_imgpath, p.detail_imgpath, p.detail_ir_imgpath from detectUserTB as d join imgPathTB as p on d.seq = p.dutseq and d.seq = %s;"
            
            curs.execute(sql, (seq))
            tupleData = curs.fetchall()
            curs.close()
            conn.close()
            return tupleData
        except Exception as e:
            print("err1",e)
    
    def getMembersData(self):
        try:
            conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
            curs = conn.cursor()
            sql = "select * from memberTB"
            
            curs.execute(sql)
            tupleData = curs.fetchall()
            curs.close()
            conn.close()
            return tupleData
        except Exception as e:
            print("err1",e)
            
    def getMemberListData(self):
        conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
        curs = conn.cursor()
        sql = "select email from memberTB"
        
        curs.execute(sql)
        tupleData = curs.fetchall()
        curs.close()
        conn.close()
        return tupleData
            
    
    def getMemberInfoAllData(self, email, dayData):
        
        conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
        curs = conn.cursor()
        sql = 'select name,dateofbirth,age,gender,userimg from memberTB where email=%s;'
        curs.execute(sql, email)
        tupleData = curs.fetchall()
        userData ={
                "name":tupleData[0][0],
                "birth":tupleData[0][1],
                "age":tupleData[0][2],
                "gender":tupleData[0][3],
                "img":tupleData[0][4]
            }
        name=tupleData[0][0]
        plotData={}
        for key in dayData:
            
            sql = 'select count(d.temp) as temp, nvl(d2.mask,0) as mask from detectUserTB as d, (select count(mask) as mask from detectUserTB where shootingDate like %s and warning = 1 and name= %s and mask=1 ) as d2 where d.shootingDate like %s and d.warning=1 and d.name=%s and d.mask=0;'
            val = (dayData[key], name, dayData[key], name)
            curs.execute(sql, val)
            tupleData = curs.fetchall()
            print(tupleData)
            plotData[key] = {"tempCnt":tupleData[0][0], "maskCnt":tupleData[0][1], "date": dayData[key].replace("%", '')}
            
        conn.close()
        return userData,plotData
    
    def getMemberVerifyData(self, email, dayData):
        conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
        curs = conn.cursor()
        plotData={}
        for key in dayData:
            sql = "select nvl(tempData.temp, 0) as temp, nvl(count(mask), 0) as mask from (select count(temp) as temp from detectUserTB as d join memberTB as m on d.memberEmail = m.email where d.shootingDate like %s and m.email=%s and mask = 0) as tempData, detectUserTB as d1 join memberTB m1 on d1.memberEmail = m1.email where d1.shootingDate like %s and m1.email=%s and mask = 1;"
            val = (dayData[key], email, dayData[key], email)
            curs.execute(sql, val)
            tupleData = curs.fetchall()
            plotData[key] = {"tempCnt":tupleData[0][0], "maskCnt":tupleData[0][1], "date": dayData[key].replace("%", '')}
        curs.close()
        conn.close()
        return plotData
    
    def warningDataUpdate(self, jsonData):
        try:
            conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
            curs = conn.cursor()
            sql = "update detectUserTB set name = %s, age= %s, gender = %s, memberEmail = %s where seq = %s;"
            val = (jsonData["name"], jsonData["age"], jsonData["gender"], jsonData["Email"], jsonData["seq"]);
            curs.execute(sql, val)
            conn.commit()
            
            sql = "insert into detectUserLogTB (dutseq, log) values (%s, %s);"
            val = (jsonData["seq"], jsonData["log"]);
            curs.execute(sql, val)
            conn.commit()
            
            curs.close()
            conn.close()
        except Exception as e:
            print("err2",e)
        
    
    def getMaskPlotData(self):
        try:
            conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
            curs = conn.cursor()
            sql = "SELECT mask, COUNT(mask) FROM detectUserTB GROUP BY mask;"
            curs.execute(sql)
            tupleData = curs.fetchall()
            curs.close()
            conn.close()
            return tupleData
        except Exception as e:
            print("err2",e)
            
    def getToDayCountData(self, now):
        try:
            conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
            curs = conn.cursor()
            sql = "select count(mask) from detectUserTB where mask =1 and shootingDate like %s;"
            curs.execute(sql, now)
            tupleData = curs.fetchall()
            dictData = {}
            dictData["mask"] = tupleData[0][0]
            sql = "select count(shootingDate) from detectUserTB where shootingDate like %s;"
            curs.execute(sql, now)
            curs.close()
            tupleData = curs.fetchall()
            dictData["tester"] = tupleData[0][0]
            conn.close()
            return dictData
        except Exception as e:
            print("err3",e)
    
    def getLogData_all(self, jsonData):
        conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
        curs = conn.cursor()
        if "mask" in jsonData:
            sql = "select dut.seq from detectUserTB as dut join memberTB as m on dut.name = m.name where m.email = %s and dut.shootingDate like %s and dut.warning = '1' and dut.mask = %s;"
            val = (jsonData['email'], jsonData['day'], jsonData["mask"])
        elif "temp" in jsonData:
            sql = "select dut.seq from detectUserTB as dut join memberTB as m on dut.name = m.name where m.email = %s and dut.shootingDate like %s and dut.warning = '1' and dut.temp > %s;"
            val = (jsonData['email'], jsonData['day'], jsonData["temp"])
        
        curs.execute(sql, val)
        tupleData = curs.fetchall()
        
        dictData = {"seq":[]}
        for index in range(len(tupleData)):
                dictData["seq"].append(tupleData[index][0])
            

        sql = "select logTB.name, logTB.temp, logTB.mask, logTB.age, logTB.gender, logTB.shootingDate, nvl(logTB.log, 'No-Log') as log, imgTB.original_IMGPath, imgTB.detail_IR_IMGPath, imgTB.original_IR_IMGPath, imgTB.detail_IMGPath FROM (select dut.seq, dut.name, dut.temp, dut.mask, dut.age, dut.gender, dut.shootingDate, dult.log from detectUserTB as dut left outer join detectUserLogTB as dult on dut.seq = dult.seq where dut.seq = %s) as logTB join imgpathTB as imgTB on imgTB.dutseq = logTB.seq;"
        val = (dictData["seq"][0])
        curs.execute(sql, val)
        tupleData = curs.fetchall()
        dictData["name"] = tupleData[0][0]
        dictData["temp"] = tupleData[0][1]
        if(tupleData[0][2] == 0):
            dictData["mask"] = "OnMask"
        else:
            dictData["mask"] = "NoMask"    
        
        dictData["age"] = tupleData[0][3]
        if(tupleData[0][4] == 0):
            dictData["gender"] = "Male"
        else:
            dictData["gender"] = "FeMale"    
        
        dictData["date"] = tupleData[0][5]
        dictData["log"] = tupleData[0][6]
        dictData["img1"] = tupleData[0][7].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img2"] = tupleData[0][8].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img3"] = tupleData[0][9].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img4"] = tupleData[0][10].replace("D:/project2021/imgFileServer/", "mntimg/")
        curs.close()
        conn.close()
        return dictData
    
    def getLogData_verify(self, jsonData):
        conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
        curs = conn.cursor()
        if "mask" in jsonData:
            sql = "select seq from detectUserTB where memberEmail = %s and shootingDate like %s and mask = %s;"
            val = (jsonData['email'], jsonData['day'], jsonData["mask"])
        elif "temp" in jsonData:
            sql = "select seq from detectUserTB where memberEmail = %s and shootingDate like %s and temp > %s;"
            val = (jsonData['email'], jsonData['day'], jsonData["temp"])
        
        curs.execute(sql, val)
        
        dictData = {"seq":[]}
        tupleData = curs.fetchall()
        for index in range(len(tupleData)):
                dictData["seq"].append(tupleData[index][0])
                

        sql = "select logTB.name, logTB.temp, logTB.mask, logTB.age, logTB.gender, logTB.shootingDate, nvl(logTB.log, 'No-Log') as log, imgTB.original_IMGPath, imgTB.detail_IR_IMGPath, imgTB.original_IR_IMGPath, imgTB.detail_IMGPath FROM (select dut.seq, dut.name, dut.temp, dut.mask, dut.age, dut.gender, dut.shootingDate, dult.log from detectUserTB as dut left outer join detectUserLogTB as dult on dut.seq = dult.seq where dut.seq = %s) as logTB join imgpathTB as imgTB on imgTB.dutseq = logTB.seq;"
        val = (dictData["seq"][0])
        curs.execute(sql, val)
        tupleData = curs.fetchall()
        dictData["name"] = tupleData[0][0]
        dictData["temp"] = tupleData[0][1]
        if(tupleData[0][2] == 0):
            dictData["mask"] = "OnMask"
        else:
            dictData["mask"] = "NoMask"    
        
        dictData["age"] = tupleData[0][3]
        if(tupleData[0][4] == 0):
            dictData["gender"] = "Male"
        else:
            dictData["gender"] = "FeMale"    
        
        dictData["date"] = tupleData[0][5]
        dictData["log"] = tupleData[0][6]
        dictData["img1"] = tupleData[0][7].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img2"] = tupleData[0][8].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img3"] = tupleData[0][9].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img4"] = tupleData[0][10].replace("D:/project2021/imgFileServer/", "mntimg/")
        curs.close()
        conn.close()
        return dictData
    
    
    def getSelectLogData(self, seq):
        conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
        curs = conn.cursor()
        dictData = {}
        sql = "select logTB.name, logTB.temp, logTB.mask, logTB.age, logTB.gender, logTB.shootingDate, nvl(logTB.log, 'No-Log') as log, imgTB.original_IMGPath, imgTB.detail_IR_IMGPath, imgTB.original_IR_IMGPath, imgTB.detail_IMGPath FROM (select dut.seq, dut.name, dut.temp, dut.mask, dut.age, dut.gender, dut.shootingDate, dult.log from detectUserTB as dut left outer join detectUserLogTB as dult on dut.seq = dult.dutseq where dut.seq = %s) as logTB join imgpathTB as imgTB on imgTB.dutseq = logTB.seq;"
        curs.execute(sql, seq)
        tupleData = curs.fetchall()
        print(tupleData)
        
        dictData["name"] = tupleData[0][0]
        dictData["temp"] = tupleData[0][1]
        if(tupleData[0][2] == 0):
            dictData["mask"] = "OnMask"
        else:
            dictData["mask"] = "NoMask"    
        
        dictData["age"] = tupleData[0][3]
        if(tupleData[0][4] == 0):
            dictData["gender"] = "Male"
        elif(tupleData[0][4] == 1):
            dictData["gender"] = "FeMale"    
        
        dictData["date"] = tupleData[0][5]
        dictData["log"] = tupleData[0][6]
        dictData["img1"] = tupleData[0][7].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img2"] = tupleData[0][8].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img3"] = tupleData[0][9].replace("D:/project2021/imgFileServer/", "mntimg/")
        dictData["img4"] = tupleData[0][10].replace("D:/project2021/imgFileServer/", "mntimg/") 
        
        
        curs.close()
        conn.close()
        return dictData
    
    def getLiveData(self, seq):
        conn = db.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db= self.__db, port=self.__port, use_unicode=True, charset='utf8')
        curs = conn.cursor()
        dictData = {}
        sql = "select seq, temp, mask, name, shootingDate, checked, warning from detectUserTB where warning = 1 and memberEmail is null and seq > %s;"
        curs.execute(sql, seq)
        tupleData = curs.fetchall()
    
        curs.close()
        conn.close()
        return tupleData