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
            self.__host = "localhost"
            self.__port = 3306
            self.__database = "TeamProject"
            self.__username = "admin"
            self.__password = "1q2w3e4r"
            cls._init = True
            
    def insertData(self, detectUserDict , imgPathDict):
        print("??")
        try:
            conn = db.connect(host=self.__host, user=self.__username, passwd=self.__password, db=self.__database, port=self.__port, use_unicode=True, charset='utf8')
            curs = conn.cursor()
            sql = "insert into detectUserTB (temp, mask, name, age, gender, shootingDate, checked, warning) values (%s, %d, %s, %s, %d, %s, %d, %d);"
            val = (detectUserDict["temp"],detectUserDict["mask"],detectUserDict["name"],detectUserDict["age"],detectUserDict["gender"],detectUserDict["shootingDate"],detectUserDict["checked"],detectUserDict["warning"])
            curs.execute(sql, val)
            imgPathDict["dutseq"] = curs.lastrowid
            sql = "insert into imgPathTB( dutseq , original_IMGPath, original_IR_IMGPath , originalDetail_IMGPath , originalDetail_IR_IMGPath) values (%d, %s, %s, %s, %s);"
            val = (imgPathDict["dutseq"],imgPathDict["original_imgpath"],imgPathDict["original_ir_imgpath"],imgPathDict["originaldetail_imgpath"],imgPathDict["originaldetail_ir_imgpath"])
            curs.execute(sql, val)
            conn.commit()
            curs.close()
            # Connection 닫기
            conn.close()
        except Exception as e :
            print(e)

        