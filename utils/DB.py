import sqlite3 as sq


def connect_db(path):
    db=sq.connect(path)
    cur=db.cursor()
    return db,cur

def close_db(db,cur):
    cur.close()
    db.close()



# l=[]
# db=sq.connect("../models/coursesInfo.db")
# #E:\Files for Work\ds proj\pdftoMySQL\coursesInfo.db
# cur=db.cursor()
#
# cursor=cur.execute("select * from 'courses'")
#
# for row in cursor:
#     # print("num: {} name:{}".format(row[0],row[1]))
#     # print(type(row[0]))
#     c=course.course(row[1], row[2], row[3], row[4], row[5])
#     l.append(c)
# for e in l:
#     print(e)
#
# cur.close()
# db.close()

