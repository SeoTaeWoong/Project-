import cv2
import pymysql as db


__host = "192.168.137.1"
__port = 3306
__database = "teamproject"
__username = "admin"
__password = "1q2w3e4r"

#sql = "insert into detectTB (name, original_path, human_path, amg8833_path, amg8833_rect_path, amgAverage, amgData, shootingTime) values (%s,%s,%s,%s,%s,%s,%s,%s);"
#val = ('JangYungDae', 'D:/project2021/imgFileServer/2022/02/03/10-55-35/fullImg.jpg', 'D:/project2021/imgFileServer/2022/02/03/10-55-35/humanImg.jpg', 'D:/project2021/imgFileServer/2022/02/03/10-55-35/amg8833.jpg', 'D:/project2021/imgFileServer/2022/02/03/10-55-35/amg8833Rect.jpg', 15.0, str([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 25.25, 25.0, 25.25, 27.25, 26.5, 0.0, 0.0, 0.0, 0.0, 25.5, 25.25, 27.0, 27.0, 27.0, 0.0, 25.5, 0.0, 0.0, 25.25, 27.25, 27.5, 26.75, 0.0, 0.0, 0.0, 0.0, 26.25, 27.5, 27.5, 26.0, 0.0, 0.0]), '2022/02/03 10:55:35')

try:
    conn = db.connect(host=__host, user=__username, passwd=__password, db=__database, port=__port, use_unicode=True, charset='utf8')
    curs = conn.cursor()
    
    
    sql = "select * from detectTB"
    print("err1")
    #curs.execute(sql, val)
    curs.execute(sql)
    conn.commit()
    tupleData = curs.fetchall()
    print(tupleData)

except Exception as e:
    print(e)
    pass

finally:
    conn.close()
    
