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
        #少create basic Table
        close_db(db,cur)
    return


