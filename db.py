import pymysql
import os

MYSQL_INFO = os.getenv('MYSQL_INFO') 
host, port, user, passwd, db = MYSQL_INFO.split('@')

conn = pymysql.connect(host = host,
                       port = int(port), user = user, 
                       passwd = passwd, db = db,
                       use_unicode = True, charset = 'utf8')

cur = conn.cursor()

def select_user_viacid(cid, cur):
    stu = cur.execute("select * from students where cid=" + str(cid))
    if stu is not None:
        info = cur.fetchone()
        return info
    else:
        return None

def insert_students(stus, cur):
    try:
        for stu in stus:
            cur.execute("insert into students (cid, name, college, politic, gender, "
                        "major, birth, national, grade, home) values " + "('" +
                        str(stu[0]) + "','" + str(stu[1]) + "','" + 
                        str(stu[2]) + "','" + str(stu[3]) + "','" + 
                        str(stu[4]) + "','" + str(stu[5]) + "','" + 
                        str(stu[6]) + "','" + str(stu[7]) + "','" + 
                        str(stu[8]) + "','" + str(stu[9]) + "');")
    except pymysql.err.IntegrityError as err:
        pass
    conn.commit()
