import sqlite3
import sqlite3 as sq
from .files import check_dir


def connect_db(path):
    db=sq.connect(path)
    cur=db.cursor()
    return db,cur


def close_db(db,cur):
    cur.close()
    db.close()


def init_db(db_dir,db_name):
    if check_dir(db_dir,db_name) is False:
        db,cur=connect_db(db_dir+'/'+db_name)
        # 少create basic Table
        close_db(db,cur)
    return

def check_table_exist(cur,table_name=''):
    sql="select count(*) from sqlite_master where type='table' and name='"+table_name+"'"
    cur.execute(sql)
    count=cur.fetchone()[0]
    return count>0
def check_table_empty(cur,table_name):
    sql='select count(*) from '+table_name+';'
    cur.execute(sql)
    count=cur.fetchone()[0]
    return count==0
def plan2DB(plan,con,plan_id):
    cursor=con.cursor()
    course_list=[]
    l=len(plan)
    for i in range(l):
        for c in plan[i]:
            course_list.append(tuple(plan_id,i+1,c.courseID))
    if not check_table_exist(con,'plans'):
        cursor.execute('''
            create table plans(
             plan_id integer,
             term integer,
             course_id text
        )''')
    sql='insert into plans (plan_id,term,courses_id) values (?,?,?);'
    try:
        cursor.executemany(sql,course_list)
    except sqlite3.Error as e:
        print(e)
        con.rollback()
        return False
    return True


