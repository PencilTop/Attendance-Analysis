import datetime
from clerk import Clerk
from enums import *
from read_ref_table import RefTable
from read_attendance_file import ReadAttendance
import clerk
from collections import namedtuple

class Attendance:
    def __init__(self, attendanceRecords, leaveRecord=None):
        self.attendanceRecords = list(attendanceRecords)
        self.leaveRecord = leaveRecord
#        self.getArriveAndLeaveTime()
#        self.getAttendanceResult()
    
    def clearAttendanceRecords(self):
        pass                                                                                      
    
    def getArriveAndLeaveTime(self):
        if self.leaveRecord != None and self.leaveRecord.LeavePeriod == LeavePeriod.WD:
            self.arriveTime = None
            self.leaveTime = None
        elif self.attendanceRecords is None:
            self.arriveTime = None
            self.leaveTime = None
        else:
            self.attendanceRecords.sort(key=lambda attRecord : attRecord.AttendanceTime)
            self.arriveTime = self.attendanceRecords[0].AttendanceTime
            self.leaveTime = self.attendanceRecords[-1].AttendanceTime
    
    def getAttendanceId(self):
        self.attendanceId = list(self.attendanceRecords)[0].attendanceId
    
    def getAttendanceResult(self):
        regularArriveTime = datetime.time.fromisoformat('09:00')
        regularLeaveTime = datetime.time.fromisoformat('17:00')
        def timeContrast():
            if self.arriveTime is None or self.leaveTime is None or self.arriveTime == self.leaveTime:
                self.attendanceResult = AttendanceResult.RecordIncomplete
            elif self.arriveTime.time() > regularArriveTime:
                self.attendanceResult = AttendanceResult.Late
            elif self.leaveTime.time() < regularLeaveTime:
                self.attendanceResult = AttendanceResult.LeaveEarly
            else:
                self.attendanceResult = AttendanceResult.Normal
        
        if self.leaveRecord is None:
            timeContrast()
        elif self.leaveRecord.LeavePeriod == LeavePeriod.WD:
            self.attendanceResult = AttendanceResult.Normal
        elif self.leaveRecord.LeavePeriod == LeavePeriod.AM:
            regularArriveTime = datetime.time.fromisoformat('13:30')
            timeContrast()
        elif self.leaveRecord.LeavePeriod == LeavePeriod.PM:
            regularLeaveTime = datetime.time.fromisoformat('11:30')
            timeContrast()
        else:
            self.attendanceResult = AttendanceResult.Unkown
        
class ClerkAttendance:
    def __init__(self, clerk, month):
        self.clerk = clerk
        self.month = month
        self.getWorkingDays()
        
    def getWorkingDays(self):
        allDays = RefTable.getDaysByMonth(self.month)
        self.workingDays = []
        if self.clerk.isNewHired == True:
            for d in allDays:
                if d.Date >= self.clerk.getHiredDate():
                    self.workingDays.append(d)
        elif self.clerk.hasResigned == True:
            for d in allDays:
                if d.Date <= self.clerk.getResignationDate():
                    self.workingDays.append(d)
        else:
            self.workingDays = list(allDays)
        
    def getAttendances(self):
        clerkAttendanceRecord = namedtuple('ClerkAttendanceRecord', ['Date',
                                                                     'Weekday',
                                                                     'DayProperty',
                                                                     'Name',
                                                                     'HasLeave',
                                                                     'LeaveProperty',
                                                                     'LeavePeriod',
                                                                     'ArriveTime',
                                                                     'LeaveTime',
                                                                     'AttendanceResult',
                                                                     'Remark'])
        
        for day in self.workingDays:
            clerkAttendanceRecord.Date = day.Date
            clerkAttendanceRecord.Weekday = day.Weekday.name
            clerkAttendanceRecord.DayProperty = day.DayProperty.name
            if day.DayProperty == DayProperty.WorkingDay:
                attRecords = ReadAttendance(self.month).getAttendanceRecordByNameAndDate(self.clerk.name, day.Date)
                leaveRecord = RefTable.getLeaveRecordByNameAndDate(self.clerk.name, day.Date)
                attendance = Attendance(attRecords, leaveRecord)
                attendance.getArriveAndLeaveTime()
                attendance.getAttendanceResult()                
                
                clerkAttendanceRecord.Name = self.clerk.name
                if leaveRecord is not None:
                    clerkAttendanceRecord.HasLeave = 'YES'
                    clerkAttendanceRecord.LeaveProperty = leaveRecord.LeaveProperty.name
                    clerkAttendanceRecord.LeavePeriod = leaveRecord.LeavePeriod.name
                else:
                    clerkAttendanceRecord.HasLeave = ''
                    clerkAttendanceRecord.LeaveProperty = ''
                    clerkAttendanceRecord.LeavePeriod = ''
                if attendance.arriveTime != None:
                    clerkAttendanceRecord.ArriveTime = attendance.arriveTime.time()
                else:
                    clerkAttendanceRecord.ArriveTime = ''
                if attendance.leaveTime != None:
                    clerkAttendanceRecord.LeaveTime = attendance.leaveTime.time()
                else:
                    clerkAttendanceRecord.LeaveTime = ''
                clerkAttendanceRecord.AttendanceResult = attendance.attendanceResult.name
                if self.clerk.isNewHired and self.clerk.getHiredDate() == day.Date:
                    clerkAttendanceRecord.Remark = 'New Hired'
                elif self.clerk.hasResigned and self.clerk.getResignationDate() == day.Date:
                    clerkAttendanceRecord.Remark = 'Has Resigned'
                else:
                    clerkAttendanceRecord.Remark = ''
            else:
                clerkAttendanceRecord.HasLeave = ''
                clerkAttendanceRecord.LeavePeriod = ''
                clerkAttendanceRecord.LeaveProperty = ''
                clerkAttendanceRecord.ArriveTime = ''
                clerkAttendanceRecord.LeaveTime = ''
                clerkAttendanceRecord.AttendanceResult = AttendanceResult.Normal.name
                clerkAttendanceRecord.Remark = ''
            yield clerkAttendanceRecord
                          
    
        
if __name__=='__main__':
    clerk = RefTable.readClerkByName('刘治君')
    clerkAttendance = ClerkAttendance(clerk, 4)
    for clerkAttendanceRecord in list(clerkAttendance.getAttendances()):
        print(clerkAttendanceRecord.Date, clerkAttendanceRecord.DayProperty, clerkAttendanceRecord.Weekday,
              clerkAttendanceRecord.Name, clerkAttendanceRecord.HasLeave, clerkAttendanceRecord.LeaveProperty, 
              clerkAttendanceRecord.LeavePeriod, clerkAttendanceRecord.ArriveTime, clerkAttendanceRecord.LeaveTime, 
              clerkAttendanceRecord.AttendanceResult, clerkAttendanceRecord.Remark)
              

"""    
    d = datetime.date.fromisoformat('2019-04-18')
    name = '胡广辉'
    readAttendance = ReadAttendance(month=4)
    attRecords = readAttendance.getAttendanceRecordByNameAndDate(name, d)
    leaveRecord = RefTable.getLeaveRecordByNameAndDate(name, d)
    attendance = Attendance(d, attRecords, leaveRecord)
    attendance.getArriveAndLeaveTime()
    attendance.getAttendanceResult()
    print(attendance.arriveTime, attendance.leaveTime)
    print(attendance.attendanceResult)
"""

    
    
    
        



