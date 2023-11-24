import sqlite3
import sqlite3 as sq
from .files import check_dir
from models import course


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
        # 少create basic Table???
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


def plan2DB(plan,con,cur,plan_id,chosen):
    cursor=con.cursor()
    course_list=[]
    l=len(plan)
    for i in range(l):
        for c in plan[i]:

            # course_list.append(tuple([plan_id, i + 1, c[0],c[1]]))
            course_list.append(tuple([plan_id, i + 1, c.courseID,int(c.name in chosen)]))
    if not check_table_exist(cur,'plans'):
        cursor.execute('''
            create table plans(
             plan_id integer,
             term integer,
             course_id text,
             chosen integer
        )''')
    sql='insert into plans (plan_id,term,course_id,chosen) values (?,?,?,?);'
    try:
        cursor.execute('select count(*) from plans where plan_id='+str(plan_id)+';')
        count=cursor.fetchone()[0]
        if count!=0:
            print('delete needed')
            cursor.execute('delete from plans where plan_id='+str(plan_id)+';')
        cursor.executemany(sql,course_list)
    except sqlite3.Error as e:
        print('error:')
        print(e)
        con.rollback()
        return False
    con.commit()
    return True


def DB2plan(plan_id,cur,major_name):
    plan=[]
    cursor=cur.execute('''select major.courseID,major.name,major.final,major.credit,major.department,major.compulsory,plans.chosen,plans.term
                        from plans
                        join {} as major on plans.course_id=major.courseID and plans.plan_id={};'''.format(major_name,plan_id))
    print('in DB3plan now!!')
    temp=[]
    chosen=[]
    for row in cursor:
        # print(row[0]+' '+row[1]+' '+row[3])
        c=course.course(row[0],row[1],row[2],row[3],row[4],row[5])
        if row[7]>len(plan)+1:
            plan.append(temp)
            temp=[]
        temp.append(c)
        if row[6]: chosen.append(c.name)
    plan.append(temp)
    return plan,chosen


def get_courseID(course_name,cur,major):
    sql='select courseID from '+major+' where name="'+course_name+'";'
    cur.execute(sql)
    id=cur.fetchone()[0]
    return id


def get_course_name(courseID,cur,major):
    cur.execute('select courseID from '+major+' where courseID='+courseID+';')
    name=cur.fetchone()[0]
    return name





