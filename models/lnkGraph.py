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
    # TODO 
    def find_all_pre(self,ver):
        for lnk in self.graph:
        pass


    def is_empty(self):
        return self.size==0

    def add_edge(self,from_ver,to_ver):
        self.graph[from_ver].append(to_ver) # 链表中是所有后续课程
        # self.graph[to_ver].append(to_ver) # 链表中是前置课程
        self.indegree[to_ver]+=1
        self.edge_num+=1

    def del_edge(self,from_ver,to_ver):
        self.graph[from_ver].del_node(to_ver)

    def find_ver_by_ID(self,id):
        l=len(self.graph)
        for e in range(l):
            if self.graph[e].head.ele.courseID==id:
                return e
        return -1
    def find_next_after(self,num):
        course_node = self.graph[num]
        res=[]
        if course_node.size==1:
            return []
        n=course_node.head.next
        while n:
            res.append(n.ele)
            n = n.next
        return res

    def find_all_after(self,num,ref):
        course_node=self.graph[num]
        pre_list=[]
        res=[]
        if course_node.size==1:
            # print("No need to find")
            return []
        n=course_node.head.next
        while n:
            # pre_list.append(n.ele)
            if n.ele not in ref:
                res.append(n.ele)
                res+=self.find_all_after(n.ele,res)
            n = n.next
        # while len(pre_list):
        #     course_index=pre_list.pop()
        #     if self.graph[course_index].size==1:
        #         continue
        #     n=self.graph[course_index].head.next
        #     while n:
        #         res.append(n.ele)
        #         pre_list.append(n.ele)
        #         n=n.next
        return res

    def find_ver_by_name(self,name):
        l=len(self.graph)
        for e in range(l):
            if self.graph[e].head.ele.name==name:
                return self.graph[e].head.ele
        return False

    def find_ver_num_by_name(self,name):
        l=len(self.graph)
        for e in range(l):
            if self.graph[e].head.ele.name==name:
                return e
        return False

    def show_ver(self):
        for v in self.graph:
            v.show()


    def in_degree(self,index):
        return self.indegree[index]

    def del_ver(self,index):
        self.graph.pop(index)

# if __name__=="__main__":
#     g=lnkGraph()