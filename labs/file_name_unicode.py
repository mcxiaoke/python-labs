#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-09 20:46:37

import os
import sys
from os import path


def handler(arg, dirname, names):
    print "process dir: %s" % dirname
    for name in names:
        filename = path.join(dirname, name)
        print "process file: %s" % filename

print sys.getdefaultencoding()
print sys.stdin.encoding
print sys.stdout.encoding
print sys.stderr.encoding


if len(sys.argv) < 2:
    sys.exit(1)

# 如果这里不提前转换为unicode
# 在Sublime的console里无法显示中文文件名
root = unicode(path.abspath(sys.argv[1]))
os.path.walk(root, handler, ())
