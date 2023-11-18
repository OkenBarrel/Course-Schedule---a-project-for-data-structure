from models.Queue import *
from models import lnkGraph

UNVISITED=0
VISITED=1


def topoSort(lnkGraph:lnkGraph.lnkGraph,limits={}):
    res=[]
    l=len(lnkGraph.graph)
    visited=[UNVISITED]*l
    indegree=lnkGraph.indegree
    in0=Queue()
    temp=[]
    credit=0
    for e in range(l):
        if indegree[e]==0:
            in0.push(e)
    while not in0.is_empty():
        ver=in0.dequeue()
        node=lnkGraph.graph[ver].head.next
        while node:
            indegree[node.ele]-=1
            if indegree[node.ele]==0:
                in0.push(node.ele)
            node=node.next
        # lnkGraph.graph[ver].show()
        course=lnkGraph.graph[ver].head.ele
        if course.compulsory:
            credit += float(course.credit)
        else:
            credit+=float(course.credit)/2
        if credit<=17.5:
            temp.append(course)
        else:
            res.append(temp)
            temp= [course]
            credit=float(course.credit)
        # lnkGraph.del_ver(ver)
        visited[ver]=VISITED
    res.append(temp)
    for ind in visited:
        if ind==UNVISITED:
            print("Error!!!")
    return res
