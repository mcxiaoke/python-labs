# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import m2
from m1 import cal

#
print(cal.add10(123))
print(cal.hello("python"))
print(m2.mul.fib(100))

# while True:
#     try:
#         x = int(raw_input("Please input a number:"))
#         print "number you input is ", x
#         break
#     except ValueError as e:
#         print e.message
#         print "Oops, invalid number, try again!"

# import sys,os
#
# print os.getcwd()
#
# try:
#     f = open('myfile.txt','r+w')
#     f.write('10000')
#     f.flush()
#     f.close()
#     f=open("myfile.txt")
#     s = f.readline()
#     i = int(s.strip())
# except IOError as e:
#     print "I/O error({0}): {1}".format(e.errno, e.strerror)
# except ValueError:
#     print "Could not convert data to an integer."
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
# else:
#     print "read value is ",i
# finally:
#     print 'GoodBye!'
