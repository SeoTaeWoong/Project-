import pymysql as db

conn = db.connect(host="192.168.137.1", user="admin", passwd="1q2w3e4r", db= "teamproject", port=3306, use_unicode=True, charset='utf8')
curs = conn.cursor()
sql = "insert into testTB (temp, mask, name, age, gender, shootingDate, checked, warning) values ('1', 0, '1', '2', 0, '2', 0, 0);"
curs.execute(sql)
print(curs.lastrowid)
conn.commit()
conn.close()

