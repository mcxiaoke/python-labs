#-*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

# tempfile用于生成临时文件和目录，兼容所有操作系统，
# 临时文件默认权限是w+b，可以指定前缀和后缀，以及文本/二进制模式

import tempfile
tempfile.mktemp() # 返回临时文件路径str对象，已不建议使用
# out: '/var/folders/53/n994f2492dz6zx4f6x812xvh0000gp/T/tmpL5_DbP'
tempfile.mkstemp() # 反文件描述符和路径组成的猿族
# out: (5, '/var/folders/53/n994f2492dz6zx4f6x812xvh0000gp/T/tmphaelRl')

tempfile.mkstemp(suffix='.tempfile',prefix='hello_') # 支持前缀和后缀
# out: (8, '/var/folders/53/n994f2492dz6zx4f6x812xvh0000gp/T/hello_Q1h82R.tempfile')
tempfile.mkstemp(suffix='.tempfile',prefix='hello_', dir='.') # 支持指定目录
# out: (10, '/Users/mcxiaoke/github/python-labs/docs/hello_7Jj5A4.tempfile')

# tempfile.TemporaryFile 普通临时文件，可以指定前缀，后缀和目录
# tempfile.NamedTemporaryFile 同上，但是有name属性
# tempfile.SpooledTemporaryFile 同TemporaryFile，默认缓存在内存中，除非有操作

tempfile.mkdtemp() # 生成临时目录，返回绝对路径
# out: '/var/folders/53/n994f2492dz6zx4f6x812xvh0000gp/T/tmpTCNKID'

tempfile.tempdir #全局的临时文件目录，从环境变量读取：TMPDIR/TEMP/TMP等
tempfile.gettempdir() # 同上
# '/var/folders/53/n994f2492dz6zx4f6x812xvh0000gp/T'

tempfile.gettempprefix() # 返回默认临时文件前缀