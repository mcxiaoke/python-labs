# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/4 20:33.
__author__ = 'mcxiaoke'

# python内置类型

# 布尔值说明
# 所有的对象都可以做真值测试，用于if或while的条件判断
# 这些值被认为是false:
'''
定义，真：1或True，假：0或False
None, False
任何数值类型的零值，如 0, 0L, 0.0, 0j.
任何空序列，如 '', (), [].
任何空映射和集合，如 {}
自定义对象 __nonzero__()或__len__()返回0或False
所有其它的值都被认为是true
'''

# 布尔操作
'''
注意：这三种操作都是短路求值
x or y 含义：if x is false, then y, else x
x and y 含义：if x is false, then x, else y
not x 含义：if x is false, then True, else False
'''

# 数值类型
n = 1234
# 返回二进制表示
print bin(n)  # 0b10011010010
# 返回需要的二进制位数，不包括前导0和符号
print n.bit_length()  # 11
n = 1234567890
print bin(n)  # 0b1001001100101100000001011010010
print n.bit_length()  # 31
f = 1234.05678
# 求绝对值
print abs(-314.15926)  # out:314.15926

# 转换为bool值
print bool([])  # out:False
print bool(None)  # out:False
print bool('')  # out:False
print bool(0.0)  # out:False
print bool(['hello'])  # out:True
print bool(1234)  # out:True
print bool(3.14)  # out:True
print bool('world')  # out:True

print '内置类型'.decode('utf-8')
print u'内置类型'.encode('utf-8')

# 内存视图
# 不会复制数据，不能修改大小
m = memoryview('hello,world')
print m.readonly  # True
b = bytearray('some text')
m = memoryview(b)
# 数据长度
print len(m)  # out:9
# 修改字节
m[0] = 'S'
# 内部格式# 转换为字符串
print m.tobytes()  # out:Some text
# 转换为序列
print m.tolist()  # out:[83, 111, 109, 101, 32, 116, 101, 120, 116]

# 函数和方法
# 两种类型的函数：内置函数和用户定义的函数，两者有相同的操作，但内部实现是不同的
