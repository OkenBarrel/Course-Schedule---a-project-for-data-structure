from models.Queue import *
from models import lnkGraph

UNVISITED=0
VISITED=1


# TODO 查bug！
def topoSort(lnkGraph:lnkGraph.lnkGraph,need_change=[],limit_term=0,limit_credit=17.5):
    l=len(lnkGraph.graph)
    res=[]
    visited=[UNVISITED]*l
    indegree=lnkGraph.indegree[:]
    in0=Queue()
    next=Queue()
    temp=[]
    credit=0
    change=len(need_change)

    for e in range(l):
        if indegree[e]==0:
            in0.push(e)
    while not in0.is_empty() or not next.is_empty():
        if change:
            bl=True
            for index,a in enumerate(indegree):
                if index not in need_change:
                    bl=bl and visited[index] and visited[need_change[0]]==0
            if bl:
                print("the plan can't be made!!")
                return False
        while not in0.is_empty():
            ver = in0.dequeue()
            course = lnkGraph.graph[ver].head.ele
            node = lnkGraph.graph[ver].head.next
            # if ver==need_change[0] and len(res)==limit:
            #     temp.append(course)
            if ver in need_change and len(res)<limit_term:
                if not next.is_in(ver):
                    next.push(ver)
                continue
            if course.compulsory:
                credit += float(course.credit)
            if credit <= limit_credit:
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
            num = lnkGraph.find_ver_num_by_name(c.name)
            af = lnkGraph.find_next_after(num)
            no += af
        later=[]
        while not next.is_empty():
            v=next.dequeue()
            if v in no:
                later.append(v)
                continue
            if v in need_change and len(res)<limit_term:
                later.append(v)
                continue
            if not in0.is_in(v):
                in0.push(v)
        for e in later:
            if not next.is_in(e):
                next.push(e)
        if in0.is_empty() and not next.is_empty():
            if len(temp)!=0:
                res.append(temp)
                temp=[]
                credit=0
            t=next.dequeue()
            if not in0.is_in(t):
                in0.push(t)
    res.append(temp)
    for ind in visited:
        if ind==UNVISITED:
            print("Error!!!")
            return False
    return res
