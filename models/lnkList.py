from models.lnkNode import *
class lnkList:
    def __init__(self,ele=None):
        self.head=lnkNode(ele)
        self.size=1

    def append(self,ele):
        if self.size==0:
            self.head=lnkNode(ele)
        else:
            h=self.head
            while h.next!=None:
                h=h.next
            h.next=lnkNode(ele)

    def size(self):
        return self.size

    def is_empty(self):
        return self.head is None

    def show(self):
        if self.is_empty():
            print("nothing to show")
            return
        l=self.head
        while l:
            l.show()
            l=l.next

    def del_node(self,ele):
        if self.head.ele==ele:
            self.head=self.head.next
        else:
            n=self.head
            while n.next:
                if n.next.ele==ele:
                    n.next=n.next.next

