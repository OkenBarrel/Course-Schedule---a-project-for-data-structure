from models.Queue import *
from models import lnkGraph

UNVISITED=0
VISITED=1


def topoSort(lnkGraph:lnkGraph.lnkGraph,old=[]):
    res=old[:]
    l=len(lnkGraph.graph)
    visited=[UNVISITED]*l
    indegree=lnkGraph.indegree
    in0=Queue()
    next=Queue()
    temp=[]
    credit=0
    cnt=0
    for e in range(l):
        if indegree[e]==0:
            in0.push(e)
    while not in0.is_empty():
        while not in0.is_empty():
            ver = in0.dequeue()
            course = lnkGraph.graph[ver].head.ele
            node = lnkGraph.graph[ver].head.next
            if course.name == '大学物理Ⅰ-2':
                print('dawu')
            if course.compulsory:
                credit += float(course.credit)
            else:
                credit += float(course.credit) / 2
            if credit <= 17.5:
                temp.append(course)
            else:
                res.append(temp)
                temp = [course]
                credit = float(course.credit)
            visited[ver] = VISITED
            while node:
                name = lnkGraph.graph[node.ele].head.ele.name
                indegree[node.ele] -= 1
                if indegree[node.ele] == 0:
                    next.push(node.ele)
                node = node.next
        no = []
        for c in temp:
            if c.name == "大学物理Ⅰ-2":
                print("yes")
            num = lnkGraph.find_ver_num_by_name(c.name)
            af = lnkGraph.find_next_after(num)
            no += af
        later=[]
        while not next.is_empty():
            ver=next.dequeue()
            if ver in no:
                later.append(ver)
                continue
            in0.push(ver)
        for e in later:
            next.push(e)
        if in0.is_empty() and not next.is_empty():
            if len(temp)!=0:
                res.append(temp)
                temp=[]
                credit=0
            t=next.dequeue()
            in0.push(t)

    res.append(temp)
    # while not next.is_empty() or not in0.is_empty():
    #     no = []
    #     for c in temp:
    #         if c.name == "大学物理Ⅰ-2":
    #             print("yes")
    #         num = lnkGraph.find_ver_num_by_name(c.name)
    #         af = lnkGraph.find_next_after(num)
    #         no += af
    #     no2 = [lnkGraph.graph[n].head.ele.courseID for n in no]
    #     while not next.is_empty():
    #         ver=next.dequeue()
    #         course = lnkGraph.graph[ver].head.ele
    #         if course.courseID in no2:
    #             in0.push(ver)
    #             continue
    #         node = lnkGraph.graph[ver].head.next
    #         if course.name=='大学物理Ⅰ-2':
    #             print('dawu')
    #         if course.compulsory:
    #             credit += float(course.credit)
    #         else:
    #             credit += float(course.credit) / 2
    #         if credit <= 17.5:
    #             temp.append(course)
    #         else:
    #             res.append(temp)
    #             temp = [course]
    #             credit = float(course.credit)
    #         # lnkGraph.del_ver(ver)
    #         visited[ver] = VISITED
    #         while node:
    #             indegree[node.ele] -= 1
    #
    #             if ver not in temp and indegree[node.ele]==0:
    #                 in0.push(node.ele)
    #             node = node.next
    #         # in0.push(node.ele)
    #     no = []
    #     for c in temp:
    #         if c.name == "大学物理Ⅰ-2":
    #             print("yes")
    #         num = lnkGraph.find_ver_num_by_name(c.name)
    #         af = lnkGraph.find_next_after(num)
    #         no += af
    #     no2 = [lnkGraph.graph[n].head.ele.courseID for n in no]
    #     while not in0.is_empty():
    #         ver=in0.dequeue()
    #         # no=[]
    #         course = lnkGraph.graph[ver].head.ele
    #         # for c in temp:
    #         #     if c.name=="大学物理Ⅰ-2":
    #         #         print("yes")
    #         #     num=lnkGraph.find_ver_num_by_name(c.name)
    #         #     no+=lnkGraph.find_next_after(num)
    #         # no2=[lnkGraph.graph[num].head.ele.courseID for num in no]
    #         if course.courseID in no2:
    #             next.push(ver)
    #             continue
    #
    #         node=lnkGraph.graph[ver].head.next
    #         if course.name=='大学物理Ⅰ-2':
    #             print('dawu')
    #         if course.compulsory:
    #             credit += float(course.credit)
    #         else:
    #             credit += float(course.credit) / 2
    #         if credit <= 17.5:
    #             temp.append(course)
    #         else:
    #             res.append(temp)
    #             temp = [course]
    #             credit = float(course.credit)
    #         # lnkGraph.del_ver(ver)
    #         visited[ver] = VISITED
    #         while node:
    #             name=lnkGraph.graph[node.ele].head.ele.name
    #             indegree[node.ele]-=1
    #             if ver not in temp and indegree[node.ele]==0:
    #                 next.push(node.ele)
    #             node=node.next
    #             # indegree[ver]=-1
    #         # lnkGraph.graph[ver].show()
    for ind in visited:
        if ind==UNVISITED:
            print("Error!!!")
    return res
