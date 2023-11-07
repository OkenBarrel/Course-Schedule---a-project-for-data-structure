import unittest
from utils import DB




class MyTestCase(unittest.TestCase):
    # def setUp(self) -> None:
    db_path = '../models/test.db'
    def print_table(self,table_name,db_path):
        print('printing: '+table_name)
        sql='select * from '+table_name+';'
        db,cur=DB.connect_db(db_path)
        cursor=cur.execute(sql)
        for row in cursor:
            print(row)
        DB.close_db(db,cur)
    def test_print_table(self):
        db_path='../models/test.db'
        # self.print_table("plan2021_prerequisites",self.db_path)
        self.print_table("计算机",self.db_path)

    def test_check_table_exist_pass(self):
        db,cur=DB.connect_db(self.db_path)
        res=DB.check_table_exist(cur,"计算机")
        DB.close_db(db,cur)
        self.assertTrue(res)

    def test_check_table_empty_pass(self):
        db,cur=DB.connect_db(self.db_path)
        res=DB.check_table_empty(cur,'plan2021_prerequisites')
        self.assertTrue(res)
        DB.close_db(db,cur)

    def test_check_table_empty_fail(self):
        db, cur = DB.connect_db(self.db_path)
        res = DB.check_table_empty(cur, 'plan2021')
        self.assertTrue(res)
        DB.close_db(db, cur)

    def test_database(self):
        major_name='计算机'
        plan_id=1
        db,cur=DB.connect_db(self.db_path)
        cur.execute('select count(*) from plans where plan_id='+str(plan_id))
        print(cur.fetchone())
        cursor = cur.execute('''select major.courseID,major.name,major.final,major.credit,major.department,major.compulsory
                                from plans
                                join {} as major on plans.course_id=major.courseID and plans.plan_id={};'''.format(major_name,plan_id))
        for row in cursor:
            print(row[0]+' '+row[1]+' '+row[2]+' '+str(row[5]==1))

if __name__ == '__main__':
    unittest.main()
