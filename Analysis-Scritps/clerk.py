from datetime import date

class Clerk:
    def __init__(self, name):
        self.name = name
        self.isNewHired = False
        self.__hiredDate = None
        self.hasResigned = False
        self.__resignationDate = None
        self.department = None
        
    
    def setHiredDate(self, date):
        if self.isNewHired:
            self.__hiredDate = date
    def getHiredDate(self):
        return self.__hiredDate
    
    def setResignationDate(self, date):
        if self.hasResigned:
            self.__resignationDate = date
    def getResignationDate(self):
        return self.__resignationDate
    
    def __repr__(self):
        clerkStr = 'Name : ' + self.name
        if self.isNewHired:
            clerkStr += '\n' + 'New hired, hired date : ' + str(self.__hiredDate)
        if self.hasResigned:
            clerkStr += '\n' + 'Has resigned, resignation date : ' +str(self.__resignationDate)
        return clerkStr
            
            
if __name__=='__main__':
    c = Clerk('胡广辉')
    c.isNewHired = True
    c.setHiredDate(date(2018, 11, 2))
    print(c)
    d = Clerk('金一鸣')
    d.hasResigned = True
    d.setResignationDate(date(2019, 6, 2))
    print(d)
    
            
        
    
            
    
    
    

















