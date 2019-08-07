from enum import Enum, unique

@unique
class Month(Enum):
    Jan = 1
    Feb = 2
    Mar = 3
    Apr = 4
    May = 5
    June = 6
    July = 7
    Aug = 8
    Sept = 9
    Oct = 10
    Nov = 11
    Dec = 12

@unique
class Weekday(Enum):
    Sun = 7
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

@unique    
class DayProperty(Enum):
    WorkingDay = 0
    Weekend = 1
    LegalHoliday = 2
    
    
@unique
class LeaveProperty(Enum):
    Rest = 0
    Vacate = 1
    Leave = 2
    
@unique
class LeavePeriod(Enum):
    WD = 0
    AM = 1
    PM = 2    

@unique
class AttendanceResult(Enum):
    Normal = 0
    Late = 1
    LeaveEarly = 2
    RecordIncomplete = 3
#    NoAMRecord = 4
#    NoPMRecord = 5
    Unkown = 99
    

    
if __name__=='__main__':
    print(Month.Aug.value)
    print(DayProperty.Weekend.name)
    print(LeaveProperty.Rest)
    









