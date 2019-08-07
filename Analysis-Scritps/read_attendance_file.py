import datetime
import os
from enums import *
from read_ref_table import RefTable
from collections import namedtuple


ATT_DIR_PATH = '..'

class ReadAttendance:
    def __init__(self, month, year=datetime.date.today().year, attDir='..', encoding='cp936'):
        self.month = month
        self.year = year
        self.attDir = '..'
        self.encoding = encoding
    
    def getAttendanceFiles(self):
        dirStr = str(self.year) + '年' + str(self.month) + '月'  + '考勤数据'
        attDir = os.path.join(self.attDir, dirStr)
        for file in os.listdir(attDir):
            if file.startswith(str(self.year)+str(self.month).zfill(2)):
                yield os.path.join(attDir, file)
    
    def getAllAttendance(self):
        for file in self.getAttendanceFiles():
            with open(file, encoding=self.encoding) as f:
                
                for line in f.readlines():
                    attRecord = namedtuple('AttendenceRecord', ['AttendanceId',
                                                          'Name',
                                                          'AttendanceTime',
                                                          ])
                    lineSplit = line.split('\t')
                    attRecord.AttendanceId = lineSplit[0]
                    attRecord.Name = lineSplit[4].encode('utf8').decode('utf8')
                    attRecord.AttendanceTime = datetime.datetime.fromisoformat(lineSplit[1])
                    yield attRecord
    
    def getAttendanceRecordByNameAndDate(self, name, date='wholemonth'):
        if date == 'wholemonth':
            days = [d.Date for d in RefTable.getDaysByMonth(self.month)]
        else:
            days = [date, ]
        for day in days:
            for record in self.getAllAttendance():
                if record.Name == name and record.AttendanceTime.date() == day:
                    yield record
    
    
if __name__=='__main__':
#    print([d.Date for d in RefTable.getDaysByMonth('Apr')])
    readAttendance = ReadAttendance(month=4)
#    for f in readAttendance.getAttendanceFiles():
#        print(f)
#    for record in readAttendance.getAllAttendance():
#        print(record.AttendanceId, record.Name, record.AttendanceTime)
    for record in readAttendance.getAttendanceRecordByNameAndDate('王瑞琛'):
        print(record.AttendanceId, record.Name, record.AttendanceTime)
    print('结束')









