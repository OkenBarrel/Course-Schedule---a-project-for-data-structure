from models import course,lnkGraph
from context import utils
from controllers import topoSort
from utils import DB
import unittest


class test_topoSort(unittest.TestCase):
    def test_topoSort_with_courses_graph_with_no_custom_setting(self):
        # l = []
        g = lnkGraph.lnkGraph()

        db, cur = utils.DB.connect_db("../models/test.db")
        # cursor = cur.execute("select * from 计算机;")
        # for row in cursor:
        #     # print("num: {} name:{}".format(row[0],row[1]))
        #     # print(row)
        #     # id name final credits department compulsory
        #     c = course.course(row[0], row[1], row[2], row[3], row[4], row[5])
        #     # print(c)
        #     # l.append(c)
        #     g.append_ver(c)

        # sql1='''select p.courseID,count(*) as num,c.name,c.final,c.credit,c.department,c.compulsory
        # from 计算机_prerequisites as p,计算机 as c
        # where c.courseId=p.courseID
        # group by p.courseID
        # order by num;'''
        # sql2='''select * from 计算机 as c
        # where not exists (select p.courseID from  计算机_prerequisites as p
        # where c.courseId=p.courseID
        # group by p.courseID);'''
        # sql3='select * from 计算机_prerequisites;'


        cursor = cur.execute('''select * from 计算机 as c
                                where not exists (select p.courseID from  计算机_prerequisites as p 
                                where c.courseId=p.courseID 
                                group by p.courseID);''')
        for row in cursor:
            # print(row)
            c = course.course(row[0], row[1], row[2], row[3], row[4], row[5])
            g.append_ver(c)
        cursor=cur.execute('''select p.courseID,count(*) as num,c.name,c.final,c.credit,c.department,c.compulsory 
                            from 计算机_prerequisites as p,计算机 as c 
                            where c.courseId=p.courseID 
                            group by p.courseID 
                            order by num;''')
        # print('again!!!')
        for row2 in cursor:
            # print(row2)
            c = course.course(row2[0], row2[2], row2[3], row2[4], row2[5], row2[6])
            g.append_ver(c)
        # print(g.indegree)
        cursor=cur.execute('select * from 计算机_prerequisites;')
        for row in cursor:
            courseID = row[0]
            preID = row[1]
            # print(row[0]+" "+row[1])
            after_index = g.find_ver_by_ID(courseID)
            pre_index = g.find_ver_by_ID(preID)

            if pre_index and after_index:  # out degree (pre_index course) in link
                # g.graph[pre_index].append(after_index)
                g.add_edge(pre_index,after_index)
        print(g.indegree)
        g.show_ver()
        res=topoSort.topoSort(g)
        length = len(res)
        for term in range(length):
            print('term'+str(term+1))
            for c in res[term]:
                print(c)

        utils.DB.close_db(db, cur)

if __name__=='__main__':
    unittest.main()