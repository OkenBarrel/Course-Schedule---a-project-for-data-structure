from models.lnkList import *
# from models.lnkNode import *


class lnkGraph:

    def __init__(self):
        # print("lnkGraph created")
        self.graph=[]
        self.size=0
        self.edge_num=0
        self.indegree=[]

    def append_ver(self,ver):
        link=lnkList(ver)
        self.graph.append(link)
        self.size+=1
        self.indegree.append(0)

    def is_empty(self):
        return self.size==0

    def add_edge(self,from_ver,to_ver):
        self.graph[from_ver].append(to_ver)
        self.indegree[to_ver]+=1
        self.edge_num+=1

    def del_edge(self,from_ver,to_ver):
        self.graph[from_ver].del_node(to_ver)

    def find_ver_by_ID(self,id):
        l=len(self.graph)
        for e in range(l):
            if self.graph[e].head.ele.courseID==id:
                return e
        return False

    def find_ver_by_name(self,name):
        l=len(self.graph)
        for e in range(l):
            if self.graph[e].head.ele.name==name:
                return self.graph[e].head.ele
        return False

    def show_ver(self):
        for v in self.graph:
            v.show()

    def show_link(self):
        for v in self.graph:
            v.show()

    def in_degree(self,index):
        return self.indegree[index]

    def del_ver(self,index):
        self.graph.pop(index)

# if __name__=="__main__":
#     g=lnkGraph()