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
            self.__host = "192.168.137.1"
            self.__port = 3306
            self.__database = "teamproject"
            self.__username = "admin"
            self.__password = "1q2w3e4r"
            cls._init = True
    
    def insertData(self, name, imgPath, amgPath, shooting_time):
        conn = db.connect(host=self.__host, user=self.__username, passwd=self.__password, db=self.__database, port=self.__port, use_unicode=True, charset='utf8')
        #curs = conn.cursor(pymysql.cursors.DictCursor)
        curs = conn.cursor()
        sql = "insert into detectTB (name,human_path,amg8833_path,shooting_time) values (%s, %s, %s, %s)"
        val = (name, imgPath, amgPath, shooting_time)
        #sql = "select * from customer where category=%s and region=%s"
        curs.execute(sql, val)
         
        curs.commit()
        # Connection 닫기
        conn.close()

    def getPageData(self, page, num):
        conn = db.connect(self.__host, user=self.__username, passwd=self.__password, db=self.__database, port=self.__port, use_unicode=True, charset='utf8')
        #curs = conn.cursor(pymysql.cursors.DictCursor)
        curs = conn.cursor()
        sql = "select count(*) from dtectTB"
        curs.execute(sql)
        # Connection 닫기
        total = curs.fetchall()
        
        total = total[0][0]
        
        paging = total+num/num
        maxVal = page*num
        minVal = maxVal - num
        sql = "select * from detectTB order by seq desc limit "+str(minVal)+","+str(maxVal)
        curs.execute(sql)
        
        tupleData = curs.fetchall()
        
        conn.close()
        
        return tupleData, paging
        