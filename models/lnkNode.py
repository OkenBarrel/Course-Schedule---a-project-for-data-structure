class lnkNode:
    def __init__(self,ele):
        self.ele=ele
        self.next=None

    # def __init__(self):
    #     self.ele=None
    #     self.next=None
    def show(self):
        print(self.ele)