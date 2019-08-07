from datetime import date
from pprint import pprint
from read_ref_table import RefTable
from clerk import Clerk
            
class Staff:
    def __init__(self, department):
        self.department = department
        self.clerks = []
        
    def addClerk(self, clerks):
        for clerk in iter(clerks):
            self.clerks.append(clerk)
            clerk.department = self.department
    
    def addClerkByName(self, clerkNames):
        self.addClerk([RefTable.readClerkByName(clerkName) for clerkName in clerkNames])
            
    def removeClerk(self, clerkName):
        for clerk in self.clerks:
            if clerk.name == clerkName:
                self.clerks.remove(clerk)
        else:
            print('[}部门没有名为{}的职员，移除失败。'.format(
                self.department,
                clerkName))
    def __repr__(self):
        return '{} ：\n{}'.format(self.department, str(self.clerks))
            
            
            
if __name__=='__main__':
    c = Clerk('胡广辉')
    c.isNewHired = True
    c.setHiredDate(date(2018, 11, 2))
    print(c)
    d = Clerk('金一鸣')
    d.hasResigned = True
    d.setResignationDate(date(2019, 6, 2))
    print(d)
    s = Staff('运维外协组')
    s.addClerk([c, d])
    print(c.department, d.department)
    pprint(s)