class course:

    def __init__(self, courseID=None, name=None, final=None, credit=None, department=None, compulsory=0):
        self.courseID=courseID
        self.name=name
        self.final=final
        self.credit=credit
        self.department=department
        self.compulsory=compulsory

    def __str__(self):
        return "ID:{} name:{} credit:{} department:{} compulsory:{}".format(self.courseID,self.name,self.credit,self.department,self.compulsory==1)