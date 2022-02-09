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
            #self.__host = "121.139.165.163"
            #self.__port = 8486
            self.__conn = db.connect(host="192.168.137.1", user="admin", passwd="1q2w3e4r", db= "teamproject", port=3306, use_unicode=True, charset='utf8')
            cls._init = True
    
    def insertData(self, name, imgPath, amgPath, shooting_time):
        conn = db.connect(host=self.__host, user=self.__username, passwd=self.__password, db=self.__database, port=self.__port, use_unicode=True, charset='utf8')
        #curs = conn.cursor(pymysql.cursors.DictCursor)
        curs = conn.cursor()
        sql = "insert into detectTB (name,human_path,amg8833_path,shooting_time) values (%s, %s, %s, %s)"
        val = (name, imgPath, amgPath, shooting_time)
        #sql = "select * from customer where category=%s and region=%s"
        curs.execute(sql, val)
        
        
        # Connection 닫기
        conn.commit()
        conn.close()

    def getPageData(self, page, num):
        try:
            
            #curs = conn.cursor(pymysql.cursors.DictCursor)
            curs = self.__conn.cursor()
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
            
            return tupleData, paging
        except Exception as e:
            print(e)
      
    def getDetectUser(self):
        try:
            
            #curs = conn.cursor(pymysql.cursors.DictCursor)
            
            curs = self.__conn.cursor()
            sql = "select * from detectUserTB order by seq desc"
            curs.execute(sql)
            tupleData = curs.fetchall()
            curs.close()

            return tupleData
        except Exception as e:
            print("err1",e)
            
    def getInfoData(self):
        try:
            curs = self.__conn.cursor()
            sql = "select * from detectUserTB order by seq desc"
            curs.execute(sql)
            tupleData = curs.fetchall()
            curs.close()

            return tupleData
        except Exception as e:
            print("err1",e)
    
    def getMaskPlotData(self):
        try:
            
            #curs = conn.cursor(pymysql.cursors.DictCursor)
            curs = self.__conn.cursor()
            sql = "SELECT mask, COUNT(mask) FROM detectUserTB GROUP BY mask;"
            curs.execute(sql)
            tupleData = curs.fetchall()
            curs.close()
            
            return tupleData
        except Exception as e:
            print("err2",e)
            
    def getToDayCountData(self, now):
        try:
            curs = self.__conn.cursor()
            sql = "select count(mask) from detectUserTB where mask = 'false' and shootingDate like %s;"
            curs.execute(sql, "%2020/03/21%")
            tupleData = curs.fetchall()
            dictData = {}
            dictData["mask"] = tupleData[0][0]
            sql = "select count(shootingDate) from detectUserTB where shootingDate like %s;"
            curs.execute(sql, "%2020/03/21%")
            curs.close()
            tupleData = curs.fetchall()
            dictData["tester"] = tupleData[0][0]
            return dictData
        except Exception as e:
            print("err3",e)
        