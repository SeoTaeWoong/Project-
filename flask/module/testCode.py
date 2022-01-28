import cv2
import pymysql as db


__host = "192.168.137.1"
__port = 3306
__database = "teamproject"
__username = "admin"
__password = "1q2w3e4r"


try:
conn = db.connect(host=__host, user=__username, passwd=__password, db=__database, port=__port, use_unicode=True, charset='utf8')
curs = conn.cursor()
sql = "select * from detectTB order by seq desc limit "+str(0)+","+str(5)
curs.execute(sql)

tupleData = curs.fetchall()

print(tupleData)


except :
    pass

finally:
    conn.close()
    