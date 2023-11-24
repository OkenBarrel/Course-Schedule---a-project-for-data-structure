from models import course,lnkGraph
from context import utils
from controllers import topoSort
from utils import DB
import unittest


def print_plan(res):
    length = len(res)
    for term in range(length):
        credit=0
        print('term' + str(term + 1))
        for c in res[term]:
            credit+=float(c.credit)
            print(c)
        print(credit)

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
        res=[3]
        res+=self.g.find_all_after(3,res)
        print(res)
        res=list(set(res))
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
        # res2=self.g.find_next_after(24)
        print(res)
        print(self.g.indegree)
        plan=topoSort.topoSort(self.g,res,5,mode='after')
        length = len(plan)

        for term in range(length):
            print('term'+str(term+1))
            for c in plan[term]:
                print(c)
    def test_is_topo(self,plan):
        term=len(plan)
        check=[]
        no=[]
        for t in range(term-1,-1,-1):
            for course in plan[t]:
                num=self.g.find_ver_num_by_name(course.name)
                no+=list(set(self.g.find_all_pre(num)))
                for ind in range(t,term):
                    check+=[c for c in plan[ind] if c in no]
                if check:
                    return False
        return True

    def test_find_all_pre(self):
        res=self.g.find_all_pre(18)
        res+=[18]
        print(res)
        # plan = topoSort.topoSort(self.g,res,limit_term=4,mode='before')
        # length = len(plan)
        #
        # for term in range(length):
        #     print('term' + str(term + 1))
        #     for c in plan[term]:
        #         print(c)

    def test_topoSort_with_courses_graph_with_no_custom_setting(self):
        res=topoSort.topoSort(self.g)
        length = len(res)
        for term in range(length):
            print('term'+str(term+1))
            for c in res[term]:
                print(c)
    def test_topo_with_limited_credit(self):
        res=topoSort.topoSort(self.g)
        print("before!!!")
        print_plan(res)
        plan=topoSort.topoSort(self.g,limit_credit=15,base=res)
        print('after!!!')
        print_plan(plan)
        print(self.test_is_topo(res))


if __name__=='__main__':
    unittest.main()
