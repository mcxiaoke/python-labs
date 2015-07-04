# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

from datetime import date, timedelta, datetime
import time

# 常量 datetime.MINYEAR=1, datetime.MAXYEAR=9999
'''
几个类方法
datetime.date(year,month,day)
datetime.time(hour,minute,second)
datetime.datetime(year,month,day,hour,minute,second)
'''

# date对象
# timedelta对象表示两个时间或日期的差值
delta = timedelta(hours=-5)
# out: datetime.timedelta(-1, 68400)
print delta.total_seconds()
# out: -18000.0
print date.today()  # datetime.date(2015, 7, 4)
print date.fromtimestamp(time.time())  # 2015-07-04

today = date.today()
print today  # 2015-07-04
today == date.fromtimestamp(time.time())
print today  # 2015-07-04
birthday = date(today.year, 10, 01)
print birthday  # 2015-10-01
time_to_birthday = abs(birthday - today)
print time_to_birthday  # 89 days, 0:00:00

# datetime对象，类方法
# 构造函数 datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
# 返回当地时间
datetime.today()  # datetime.datetime(2015, 7, 4, 16, 32, 29, 748628)
# 返回当地时间
datetime.now()  # datetime.datetime(2015, 7, 4, 16, 32, 53, 701843)
# 返回UTC时间
datetime.utcnow()  # datetime.datetime(2015, 7, 4, 8, 34, 14, 433219)
# 根据时间戳构建当地时间
datetime.fromtimestamp(time.time())  # datetime.datetime(2015, 7, 4, 16, 34, 53, 402597)
# 根据时间戳构建UTC时间
datetime.utcfromtimestamp(time.time())  # datetime.datetime(2015, 7, 4, 8, 35, 36, 268517)
# 根据格式和日期字符串构造对象，用法同time模块的strptime()
# datetime.strptime(date_string, format)

# datetime对象，实例方法
now = datetime.now()
print now.date()  # 2015-07-04
print now.time()  # 16:45:29.077727
print now.utcoffset()  # None
print now.timetuple()
# out: time.struct_time(tm_year=2015, tm_mon=7, tm_mday=4,
# tm_hour=16, tm_min=46, tm_sec=29, tm_wday=5, tm_yday=185, tm_isdst=-1)
# 类似的还有 now.utctimetuple()
print now.__str__()  # 2015-07-04 16:48:02.930730
print now.ctime()  # 'Sat Jul  4 16:44:03 2015'
print now.strftime('%Y-%m-%d %H:%M:%S')  # 2015-07-04 16:49:25

# time对象
t = now.time()
print t.isoformat()  # 返回ISO8601格式 16:52:19.700394
print t.utcoffset()  # 返回时区偏移 None
