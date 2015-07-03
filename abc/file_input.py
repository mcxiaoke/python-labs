#-*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import os,fileinput
# 内部使用FileInput类实现
# fileinput 是一个从标准输入或者文件按行读入的工具类，默认是文本模式，一般的用法是

for line in fileinput.input(['file_input.py']):
    print fileinput.filename() # 文件名
    print fileinput.fileno() #文件描述符，int
    print fileinput.lineno() #总的行号
    print fileinput.filelineno() #当前文件的行号
    print fileinput.isstdin() # 是否标准输入
    print fileinput.isfirstline() # 是否是文件的第一行
    print fileinput.nextfile() # 关闭当前文件，开始读下一个文件
    print fileinput.close() # 关闭输入序列

