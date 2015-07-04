# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/4 17:01.
__author__ = 'mcxiaoke'

import datetime
import string
from string import Template

# 一些常量
'''
whitespace = ' \t\n\r\v\f'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = lowercase + uppercase
ascii_lowercase = lowercase
ascii_uppercase = uppercase
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + letters + punctuation + whitespace
'''

# 字符串格式化
# 字符串格式化格式为 "hello, world {0} {1}"
# 默认调用 __format()__方法，可以显示使用str()或repr()
# "Harold's a clever {0!s}"        # Calls str() on the argument first
# "Bring out the holy {name!r}"    # Calls repr() on the argument first
print "hello, world {0} {1} !".format('first', 'second')

# 字符串格式 %s
print "Welcome to %s" % "China"

# 整数格式
'''
'b' 二进制整数
'c' Unicode字符
'd' 十进制整数
'o' 八进制整数
'x' 十六进制，小写
'X' 十六进制，大写
'n' 十进制，带分隔符
'''
num = 1234567890
print "十进制:%d 八进制:%o 十六进制:0x%x 十六进制:0X%X" % (num, num, num, num)
# out: 十进制:1234567890 八进制:11145401322 十六进制:0x499602d2 十六进制:0X499602D2
# 浮点数格式
fnum = 987123456.78901234567890123
print '%e' % fnum, '%E' % fnum, '%f' % fnum, '%F' % fnum, '%g' % fnum, '%G' % fnum
# out: 9.871235e+08 9.871235E+08 987123456.789012 987123456.789012 9.87123e+08 9.87123E+08

# 格式化例子
print '{0}, {1}, {2}'.format('a', 'b', 'c')  # a, b, c
print '{}, {}, {}'.format('a', 'b', 'c')  # a, b, c
print '{2}, {1}, {0}'.format('a', 'b', 'c')  # c, b, a
print '{2}, {1}, {0}'.format(*'abc')  # 参数解包
print '{0}{1}{0}'.format('hello-', 'world-')  # 参数可以重复使用
# out: hello-world-hello-

# 命名参数例子 # out: 经纬度: (37.24N, -115.81W)
print '经纬度: ({0}, {1})'.format('37.24N', '-115.81W')
print 'A 经纬度: ({latitude}, {longitude})'.format(latitude='37.24N', longitude='-115.81W')
args = ('37.24N', '-115.81W')
print 'B 经纬度: ({}, {})'.format(*args)
kwargs = {'latitude': '37.24N', 'longitude': '-115.81W'}
print 'C 经纬度: ({latitude}, {longitude})'.format(**kwargs)

# 自定义对象例子
class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return "Point({self.x},{self.y})".format(self=self)

    def __repr__(self):
        return "(x={self.x},y={self.y})".format(self=self)


pt = Point(15, 238)
print 'Point is {}'.format(pt)  # Point is Point(15,238)
print 'Point(x={0.x}, y={0.y})'.format(pt)  # Point(x=15, y=238)
two = ('hello', 'world')
print 'A={0[0]}, B={0[1]}'.format(two)  # A=hello, B=world
# 使用 repr()和str()的示例
print "repr() shows quotes: {!r}; str() doesn't: {!s}".format('test1', 'test2')
print 'Point is {0!r} {0!s}'.format(pt)  # Point is (x=15,y=238) Point(15,238)

# 对其方式
# 星号用于加强显示效果，默认是空白
print '{:*<30}'.format('左对齐')  # 左对齐*********************
print '{:*>30}'.format('右对齐')  # *********************右对齐
print '{:*^30}'.format('居中对其')  # *********居中对其*********

# 数字格式处理
# 不带前缀
print "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format(2015)
# out: int: 2015;  hex: 7df;  oct: 3737;  bin: 11111011111
# 带前缀
print "int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}".format(2015)
# int: 2015;  hex: 0x7df;  oct: 0o3737;  bin: 0b11111011111
# 添加分隔符
print '{:,}'.format(1234567890)  # 1,234,567,890
# 日期时间格式化
d = datetime.datetime.now()
print '{:%Y-%m-%d %H:%M:%S}'.format(d)  # 2015-07-04 18:34:28

# 字符串模板
s = Template('$who likes to eat $what')
print s.substitute(who='john', what='fish')  # john likes to eat fish

# 字符串函数
s = 'this is some sample text.'
# 首字母大写
print string.capitalize(s)  # This is some sample text.
# 结果等于 s.capitalize()
# 查找字符串
print s.find('is')  # 2
print s.find('hello')  # -1
# 分割字符串
print s.split(' ')  # ['this', 'is', 'some', 'sample', 'text.']
print s.split(' ', 1)  # ['this', 'is some sample text.']
print s.rsplit(' ', 1)  # ['this is some sample', 'text.']
# 合并字符串
print s.join(['A_', 'B'])  # A_this is some sample text.B
print string.join(['there', 'are', 'joined', 'words'], ' ')  # there are joined words
s2 = 'this\tis\tsome\tsample\ttext'
# 展开TAB
print s2.expandtabs(4)  # this    is  some    sample  text
s3 = '     hello,     python!    '
# 去除前后空白
print s3.strip()  # hello,     python!
s4 = 'THIS is SOME text.'
# 交换大小写
print s4.swapcase()  # this IS some TEXT.
# 首字母大写
print s4.capitalize()  # This is some text.
# 全部小写
print s4.lower()  # this is some text.
# 全部大写
print s4.upper()  # THIS IS SOME TEXT.
# 补齐字符串
print s4.ljust(30, '_')  # THIS is SOME text.____________
print s4.rjust(30, '_')  # ____________THIS is SOME text.
print s4.center(30, '_')  # ______THIS is SOME text.______
print s4.zfill(30)  # 000000000000THIS is SOME text.
# 替换字符串
s5 = 'color1 and color2 and color3 scheme files are tested.'
print s5.replace('color', 'dark')
# out: dark1 and dark2 and dark3 scheme files are tested.
print s5.replace('and', '')
# out: color1  color2  color3 scheme files are tested.
print s5.replace(' ', '_')
# out: color1_and_color2_and_color3_scheme_files_are_tested.
print s5.replace(' ', '-', 2)
# out: color1-and-color2 and color3 scheme files are tested.
