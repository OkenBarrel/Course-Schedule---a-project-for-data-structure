from models.Queue import *

UNVISITED=0
VISITED=1
def topoSort(lnkGraph):
    res=[]
    l=len(lnkGraph.graph)
    visited=[UNVISITED]*l
    indegree=lnkGraph.indegree
    in0=Queue()
    rest=Queue()
    temp=[]
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
        if len(temp)<10:
            temp.append(lnkGraph.graph[ver].head.ele)
        else:
            res.append(temp)
            temp=[]
            temp.append(lnkGraph.graph[ver].head.ele)
        # lnkGraph.del_ver(ver)
        visited[ver]=VISITED
    for ind in visited:
        if ind==UNVISITED:
            print("Error!!!")
    for ele in res:
        print("list:")
        for el in ele:
            print(el)
