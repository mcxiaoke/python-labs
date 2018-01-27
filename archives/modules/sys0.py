# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/4 20:14.
__author__ = 'mcxiaoke'

import sys

print sys.argv  # Python脚本的命令行参数，argv[0]是脚本的名字
print sys.byteorder  # 字节序，大端还是小端 osx:little
print sys.builtin_module_names  # 内置模块列表
print sys.executable  # 返回python解释器的路径
# out: /usr/local/opt/python/bin/python2.7
# sys.exit("some error occurred")  # 退出python进程
# sys.exit(0)
# 获取某个对象的大小，单位是字节
# 仅适用于内置对象，实现是使用了对象的__sizeof__方法
print sys.getsizeof(int(123))
print sys.getsizeof(float(123))  # 24
print sys.getsizeof('s')  # 38
print sys.getsizeof(u'u')  # 52
print sys.path  # 返回搜索路径
print sys.modules  # 返回当前载入的模块列表
print sys.platform  # 返回操作系统标识
print sys.prefix  # 返回python安装路径
# out: /usr/local/Cellar/python/2.7.8_1/Frameworks/Python.framework/Versions/2.7'
print sys.version  # 安装的python版本信息
# out: 2.7.8 (default, Oct 14 2014, 11:30:30)
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.51)]
print sys.version_info  # python版本信息
# out: sys.version_info(major=2, minor=7, micro=8, releaselevel='final', serial=0)

# Python默认编码
print sys.getdefaultencoding()  # out:ascii
# 文件系统默认编码
print sys.getfilesystemencoding()  # out:utf-8
