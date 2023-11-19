from models import course,lnkGraph
from context import utils
from controllers import topoSort
from utils import DB
import unittest


class test_topoSort(unittest.TestCase):
    def setUp(self) -> None:
        self.g = lnkGraph.lnkGraph()

        self.db, self.cur = utils.DB.connect_db("../models/test.db")
        cursor = self.cur.execute('''select * from 计算机 as c
                                        where not exists (select p.courseID from  计算机_prerequisites as p 
                                        where c.courseId=p.courseID 
                                        group by p.courseID);''')
        for row in cursor:
            # print(row)
            c = course.course(row[0], row[1], row[2], row[3], row[4], row[5])
            self.g.append_ver(c)
        cursor = self.cur.execute('''select p.courseID,count(*) as num,c.name,c.final,c.credit,c.department,c.compulsory 
                                    from 计算机_prerequisites as p,计算机 as c 
                                    where c.courseId=p.courseID 
                                    group by p.courseID 
                                    order by num;''')
        # print('again!!!')
        for row2 in cursor:
            # print(row2)
            c = course.course(row2[0], row2[2], row2[3], row2[4], row2[5], row2[6])
            self.g.append_ver(c)
        # print(g.indegree)
        cursor = self.cur.execute('select * from 计算机_prerequisites;')
        for row in cursor:
            courseID = row[0]
            preID = row[1]
            # print(row[0]+" "+row[1])
            after_index = self.g.find_ver_by_ID(courseID)
            pre_index = self.g.find_ver_by_ID(preID)

            if pre_index!=-1 and after_index!=-1:  # out degree (pre_index course) in link
                # g.graph[pre_index].append(after_index)
                self.g.add_edge(pre_index, after_index)
        self.g.show_ver()
        # print(self.g.indegree)
        # DB.close_db(db,cur)
        return

    def test_graph_find_all_after(self):
        res=[1]
        res+=self.g.find_all_after(1)
        n=lnkGraph.lnkGraph()
        for num in res:
            lnk=self.g.graph[num]
            n.append_ver(lnk.head.ele)
        cursor = self.cur.execute('select * from 计算机_prerequisites;')
        for row in cursor:
            courseID = row[0]
            preID = row[1]
            # print(row[0]+" "+row[1])
            after_index = n.find_ver_by_ID(courseID)
            pre_index = n.find_ver_by_ID(preID)
            if pre_index!=-1 and after_index!=-1:  # out degree (pre_index course) in link
                # g.graph[pre_index].append(after_index)
                n.add_edge(pre_index, after_index)
        # n.show_ver()
        print(n.indegree)
        res2=self.g.find_next_after(1)
        print(res)
        print(self.g.indegree)
        plan=topoSort.topoSort(self.g,res,2)
        length = len(plan)
        for term in range(length):
            print('term'+str(term+1))
            for c in plan[term]:
                print(c)

    def test_topoSort_with_courses_graph_with_no_custom_setting(self):

        res=topoSort.topoSort(self.g)
        length = len(res)
        for term in range(length):
            print('term'+str(term+1))
            for c in res[term]:
                print(c)

if __name__=='__main__':
    unittest.main()
