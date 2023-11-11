from models.Queue import *

UNVISITED=0
VISITED=1
# FIXME topoSort: need to arrange courses in graph by prerequisites num
def topoSort(lnkGraph,one_in_a_term=None):
    only_once=['体育']
    res=[]
    l=len(lnkGraph.graph)
    visited=[UNVISITED]*l
    indegree=lnkGraph.indegree
    in0=Queue()
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
            temp= [lnkGraph.graph[ver].head.ele]
        # lnkGraph.del_ver(ver)
        visited[ver]=VISITED
    res.append(temp)
    for ind in visited:
        if ind==UNVISITED:
            print("Error!!!")
    return res
