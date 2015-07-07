# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 2015/7/7 23:33.
__author__ = 'mcxiaoke'

# 清除目录里的txt和临时文件

import os, sys
from os import path


def handler(arg, dirname, names):
    dir_path = path.join(dirname, dirname)
    for file in names:
        file_path = path.abspath(path.join(dirname, file))
        root, ext = path.splitext(file_path)
        if ext and ('.tmp' == ext or '.txt' == ext):
            os.remove(file_path)
            print "delete file: %s." % file_path


os.path.walk(path.normcase(sys.argv[1]), handler, ())
