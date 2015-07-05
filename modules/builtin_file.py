# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/5 00:17.
__author__ = 'mcxiaoke'

# 文件对象
# File对象使用C的stdio实现，可以通过open()函数创建

# 写入文件
with open('hello.txt', 'w') as f:
    print 'filename=', f.name, ',fileno=', f.fileno()
    print 'encoding=', f.encoding, 'mode=', f.mode
    # 写入序列数据，默认不会添加换行符
    f.writelines(['line 1', 'line 2', 'line 3'])
    f.flush()
    for i in range(0, 5):
        f.write(str(i))
        f.write(":som text.")
        f.write('\n')
    f.flush()
# 读取文件
with open('hello.txt') as f:
    for line in f:
        if line.strip():
            print line,
# 打开文件
f = open('hello.txt')
# 读取指定字节数
print '32bit:', f.read(32)  # out:writing t
# 读取一行
# file.readline([size])
print 'line:', f.readline()  # out:writing text for test.
# f.seek(2, os.SEEK_CUR) f.seek(-3, os.SEEK_END)
# 返回当前的偏移
print f.tell()
# 设置偏移 file.seek(offset[, whence])
f.seek(0)
# 读取所有行，可以指定最多的读取行数，不会添加换行符
# file.readlines([sizehint])
print 'lines:', f.readlines()  # out:['line','line','line']
f.close()
# 截断文件
# file.truncate([size])
f = open('hello.txt', 'r+w')
f.truncate(32)
f.close()
