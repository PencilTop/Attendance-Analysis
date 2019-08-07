import pandas as pd
from collections import namedtuple
import time, datetime
from builtins import staticmethod
from enums import *
from clerk import Clerk

EXCEL_PATH = r'../ref-table.xlsx'
STAFF_SHEET = r'AttendanceStaff'
LEAVE_SHEET = r'LeaveRecords'
DAY_SHEET = r'WorkingDays'

def counting_down(seconds):
    print('counting down...')
    for i in range(seconds, 0, -1):
        print(i, end=' ')
        time.sleep(1)
 
class RefTable:
    @staticmethod
    def readAllClerks():
        sdf = pd.read_excel(EXCEL_PATH, STAFF_SHEET).fillna('')
        for i in sdf.index:
            clerk = Clerk(sdf['Name'][i])
            if sdf['IsNewHired'][i] == 'YES':
                clerk.isNewHired = True
                clerk.setHiredDate(sdf['HiredDate'][i].date())
            if sdf['HasResigned'][i] == 'YES':
                clerk.hasResigned = True
                clerk.setResignationDate(sdf['ResignationDate'][i].date())
            yield clerk
            
    
    @staticmethod
    def readClerkByName(clerkName):
        sdf = pd.read_excel(EXCEL_PATH, STAFF_SHEET).fillna('')
        for i in sdf.index:
            if sdf['Name'][i] == clerkName:
                clerk = Clerk(clerkName)
                if sdf['IsNewHired'][i] == 'YES':
                    clerk.isNewHired = True
                    clerk.setHiredDate(sdf['HiredDate'][i].date())
                if sdf['HasResigned'][i] == 'YES':
                    clerk.hasResigned = True
                    clerk.setResignationDate(sdf['ResignationDate'][i].date())
                return clerk
         
    @staticmethod
    def getLeaveRecords():
        ldf = pd.read_excel(EXCEL_PATH, LEAVE_SHEET)
        for i in ldf.index:
            leaveRecord = namedtuple('LeavRecord', ['LeaveDate', 
                                                    'Name',
                                                    'LeavePeriod',
                                                    'LeaveProperty'])
            leaveRecord.LeaveDate = ldf['LeaveDate'][i].date()
            leaveRecord.Name = ldf['Name'][i]
            if ldf['LeavePeriod'][i] == 'WholeDay':
                leaveRecord.LeavePeriod = LeavePeriod.WD
            elif ldf['LeavePeriod'][i] == 'AM':
                leaveRecord.LeavePeriod = LeavePeriod.AM
            elif ldf['LeavePeriod'][i] == 'PM':
                leaveRecord.LeavePeriod = LeavePeriod.PM
            else:
                print('{}在{}的请假记录有错误或不完整。'.format(leaveRecord.Name,
                                                            leaveRecord.LeaveDate))
            if ldf['LeaveProperty'][i] == 'Rest':
                leaveRecord.LeaveProperty = LeaveProperty.Rest
            elif ldf['LeaveProperty'][i] == 'Vacate':
                leaveRecord.LeaveProperty = LeaveProperty.Vacate
            elif ldf['LeaveProperty'][i] == 'Leave':
                leaveRecord.LeaveProperty = LeaveProperty.Leave
            else:
                print('{}在{}的请假性质有错误或不完整。'.formate(leaveRecord.Name,
                                                            leaveRecord.LeaveDate))
            yield leaveRecord
    
    @staticmethod
    def getLeaveRecordByNameAndDate(name, date):
        for leaveRecord in RefTable.getLeaveRecords():
            if leaveRecord.Name == name and leaveRecord.LeaveDate == date:
                return leaveRecord
    
    @staticmethod
    def getLeaveRecordsByName(name):
        for record in RefTable.getLeaveRecords():
            if record.Name == name:
                yield record
            

    @staticmethod
    def getDaysByMonth(month):
        if (month not in Month.__members__.keys()) and (month not in range(1, 13)):
            return 
        if type(month) == int:
            mvalue = month
        else: 
            mvalue = dict(Month.__members__.items())[month].value
        ddf = pd.read_excel(EXCEL_PATH, DAY_SHEET)
        for i in ddf.index:
            d = ddf['Date'][i].date()
            if d.month == mvalue:
                workingDay = namedtuple('WorkingDay', ['Date',
                                                       'WeekDay',
                                                       'DayProperty'])
                workingDay.Date = d
                workingDay.Weekday = Weekday(d.isoweekday())
                if ddf['WorkingDay'][i] == 'YES':
                    workingDay.DayProperty = DayProperty.WorkingDay
                elif ddf['Weekend'][i] == 'YES':
                    workingDay.DayProperty = DayProperty.Weekend
                elif ddf['LegalHoliday'][i] == 'YES':
                    workingDay.DayProperty = DayProperty.LegalHoliday
                else:
                    print('{} 的日期性质有误，请检查。'.format(d))
                yield workingDay
                
    @staticmethod
    def getDayByDate(date):
        """
        参数date为日期字符串，格式默认为XXXX-XX-XX
        """
        d = datetime.date.fromisoformat(date)
        for day in RefTable.getDaysByMonth(Month(d.month).name):
            if day.Date == d:
                return day
        
    @staticmethod
    def getLeaveNames():
        pass
 
 
        
if __name__=='__main__':
#    counting_down(10)
#    print(list(RefTable.readAllClerks()))
#    for l in RefTable.getLeaveRecords():
#        print(l.Name, l.LeaveDate, l.LeavePeriod, l.LeaveProperty)
#    for l in RefTable.getLeaveRecordsByName('刘治君'):
#        print(l.Name, l.LeaveDate, l.LeavePeriod, l.LeaveProperty)
    for d in RefTable.getDaysByMonth(5):
        print(d.Date, d.Weekday, d.DayProperty)
#    print(RefTable.getDayByDate('2019-05-01').DayProperty)
    
    
    
    
    
    
    
    
    