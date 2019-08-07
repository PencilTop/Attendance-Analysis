import xlsxwriter
from attendance import ClerkAttendance
from clerk import Clerk
from staff import Staff
from read_ref_table import RefTable
from enums import *

def WriteRecordsToExcel(clerks, month):
    workbook = xlsxwriter.Workbook('../驻场外协{}月份考勤汇总表.xlsx'.format(month))
    
    countSheet = workbook.add_worksheet('统计汇总')
    countTitleFormat = workbook.add_format()
    countCellFormat = workbook.add_format()
    countTitleFormat.set_bold(True)
    countTitleFormat.set_font('黑体')
    countTitleFormat.set_font_size(14)
    countTitleFormat.set_bg_color('#BFEFFF')
    countTitleFormat.set_align('center')
    countTitleFormat.set_align('vcenter')
    countTitleFormat.set_text_wrap()
#    countTitleFormat.set_shrink()
    countTitleFormat.set_border()
    
    countCellFormat.set_font('宋体')
    countCellFormat.set_font_size(12)
    countCellFormat.set_align('center')
    countCellFormat.set_align('vcenter')
    countCellFormat.set_shrink()
    countCellFormat.set_border()
    countSheet.set_row(0, 40)
    countSheet.set_column(9, 9, 18)
    
    titleList = ['序号', '姓名', '工作日', '正常',
                 '休假\n(一天)', '休假\n(半天)', '打卡\n不完整', 
                 '迟到', '早退', '备注']   
    for n, t in enumerate(titleList):
        countSheet.write(0, n, t, countTitleFormat)
        
    def WriteAttendanceCountData(countSheet, seq, clerk):
        countSheet.set_row(seq, 30)
        clerkAttendance = ClerkAttendance(clerk, month)
        clerkAttendanceRecords = clerkAttendance.getAttendances()
        attDaysCount = 0
        attNomalCount = 0
        leaveWholeDaysCount = 0
        leaveHalfDaysCount = 0
        attIncompleteCount = 0
        attLateCount = 0
        attLeaveEarlyCount = 0
        name = ''
        remark = ''
        for record in clerkAttendanceRecords:
            if record.DayProperty == DayProperty.WorkingDay.name:
                attDaysCount += 1
            if record.DayProperty == DayProperty.WorkingDay.name:
                if record.AttendanceResult == AttendanceResult.Normal.name and record.LeavePeriod != LeavePeriod.WD.name:
                    attNomalCount += 1
                elif record.AttendanceResult == AttendanceResult.Late.name:
                    attLateCount += 1
                elif record.AttendanceResult == AttendanceResult.LeaveEarly.name:
                    attLeaveEarlyCount += 1
                elif record.AttendanceResult == AttendanceResult.RecordIncomplete.name:
                    attIncompleteCount += 1
    #        else:
    #            print("Unknow {}'s {} Attendance Record: {}".format(record.Name,record.Date, record.AttendanceResult))
            if record.HasLeave:
                if record.LeavePeriod == LeavePeriod.AM.name or record.LeavePeriod == LeavePeriod.PM.name:
                    leaveHalfDaysCount += 1
                elif record.LeavePeriod == LeavePeriod.WD.name:
                    leaveWholeDaysCount += 1
            name = record.Name
            if record.Remark == 'New Hired':
                remark = record.Date.isoformat()+'入职'
            elif record.Remark == 'Has Resigned':
                remark = record.Date.isoformat()+'离职'
            countSheet.write_row(seq, 0, [seq,
                                          name,
                                          attDaysCount,
                                          attNomalCount,
                                          leaveWholeDaysCount,
                                          leaveHalfDaysCount,
                                          attIncompleteCount,
                                          attLateCount,
                                          attLeaveEarlyCount,
                                          remark], countCellFormat)
   
    for i, clerk in enumerate(clerks):  
        seq = i + 1
        WriteClerkSheet(workbook, clerk, month)    
        WriteAttendanceCountData(countSheet, seq, clerk)  
        print('{} 的信息写入完成'.format(clerk.name))        
    workbook.close()

def WriteClerkSheet(workbook, clerk, month):
    clerkAttendance = ClerkAttendance(clerk, month)
    clerkAttendanceRecords = clerkAttendance.getAttendances() 
    clerkSheet = workbook.add_worksheet(clerk.name)
    clerkSheet.set_row(0, 40)
    clerkTitleFormat = workbook.add_format()
    clerkCellFormat = workbook.add_format()
    
    clerkTitleFormat.set_bold(True)
    clerkTitleFormat.set_font('Arial')
    clerkTitleFormat.set_font_size(14)
    clerkTitleFormat.set_bg_color('#ADFF2F')
    clerkTitleFormat.set_align('center')
    clerkTitleFormat.set_align('vcenter')
    clerkTitleFormat.set_border()
    
    clerkCellFormat.set_font('Consolas')
    clerkCellFormat.set_font_size(12)
    clerkCellFormat.set_align('center')
    clerkCellFormat.set_align('vcenter')
    clerkCellFormat.set_border()
#    clerkCellFormat.set_num_format()

    columnWitdthList = [15.5, 14, 20, 10, 14, 20, 16, 16, 16, 23, 14.5]
    for i, w in enumerate(columnWitdthList):
        clerkSheet.set_column(i, i, w)
       
    sheetTitle = ['Date', 'Weekday', 'DayProperty', 'Name', 'HasLeave',
                  'LeaveProperty', 'LeavePeriod', 'ArriveTime', 'LeaveTime',
                  'AttendanceResult', 'Remark']
    clerkSheet.write_row(0, 0, sheetTitle, clerkTitleFormat)
    for i, record in enumerate(clerkAttendanceRecords):
        clerkSheet.set_row(i+1, 20)
        recordList = [record.Date.isoformat(),
                      record.Weekday,
                      record.DayProperty,
                      record.Name,
                      record.HasLeave,
                      record.LeaveProperty,
                      record.LeavePeriod,
                      record.ArriveTime.isoformat() if record.ArriveTime else '',
                      record.LeaveTime.isoformat() if record.LeaveTime else '',
                      record.AttendanceResult,
                      record.Remark]
        print(recordList)
        clerkSheet.write_row(i+1, 0, recordList, clerkCellFormat)
        

if __name__=='__main__':
    staff = Staff('外协小组')
    staff.addClerkByName(['胡广辉', '刘治君', '金一鸣', '李超俊', '杜福增', '柯龙', '杨雄'])
    WriteRecordsToExcel(staff.clerks, 4)
    
    
    
    
"""        
    staff.addClerkByName(['胡广辉', '刘治君', '金一鸣', '李超俊', '杜福增', '柯龙', '杨雄',
                          '郑鹏冲','徐磊',
                          '梁峰川', '袁朝海', '华骏能', '郑毅',
                          '唐小涛', '李强', '梁超', '闫佳楠', '王瑞琛'])
""" 
    










