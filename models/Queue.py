from models.lnkNode import *

class Queue:

    def __init__(self,head=None,next=None):
        self.head=head
        self.next=next
        self.size=0

    def is_empty(self):
        return self.size==0

    def dequeue(self):
        if self.is_empty():
            print("nothing to dequeue")
            return
        res=self.head.ele
        self.head=self.head.next
        self.size-=1
        return res

    def get_frot(self):
        if self.is_empty():
            print("nothing to dequeue")
            return
        res = self.head.ele
        return res

    # def append(self,ele):
    #     if self.is_empty():
    #         self.head=lnkNode(ele)
    #     else:
    #         n=self.head
    #         while n:
    #             n=n.next
    #         n.next=lnkNode(ele)
    #     self.size += 1

    def show(self):
        n=self.head
        while n:
            n.show()
            n=n.next

    def push(self,ele):
        if self.is_empty():
            self.head=lnkNode(ele)
        else:
            n=self.head
            while n.next:
                n=n.next
            n.next=lnkNode(ele)
        self.size+=1
