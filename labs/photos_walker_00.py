# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 2015/7/6 22:20.
__author__ = 'mcxiaoke'

import sys, os
from os import path
from datetime import datetime

print 'curren dir is', os.getcwd()
print 'command line args is', sys.argv

if len(sys.argv) < 2:
    sys.exit(1)

# 批量重命名照片文件
# 根据文件修改日期重命名文件，然后移动到目标文件夹

FILE_NAME_FORMAT = "IMG_%Y%m%d_%H%M%S"
start_dir = path.abspath(sys.argv[1])
output_dir = path.join(path.dirname(start_dir), 'output')
if not path.exists(output_dir):
    os.mkdir(output_dir)
print 'start dir is %s' % start_dir
print 'output dir is %s' % output_dir

bn = []
an = []


def handler(arg, dirname, names):
    dir_path = path.join(dirname, dirname)
    print ("current dir is %s" % dir_path)
    for file in names:
        file_path = path.abspath(path.join(dirname, file))
        print "processing file: %s" % file
        # print 'path is file: ', path.isfile(file_path)
        if not path.isfile(file_path):
            continue
        _, ext = path.splitext(file)
        file_st = os.stat(file_path)
        fm = datetime.fromtimestamp(file_st.st_mtime)
        print 'file modified time is', fm.strftime("%Y-%m-%d %H:%M:%S"), fm.microsecond
        src_name = file
        dest_name = fm.strftime(FILE_NAME_FORMAT) + ext
        print 'src name is %s' % src_name
        print 'dest name is %s' % dest_name
        if src_name != dest_name:
            bn.append(path.abspath(path.join(dirname, src_name)))
            an.append(path.abspath(path.join(output_dir, dest_name)))
    return 0


os.path.walk(start_dir, handler, ())
if bn and an:
    for src, dest in zip(bn, an):
        print src, dest
        if path.exists(src) and path.isfile(src) and not path.exists(dest):
            ret = os.rename(src, dest)
            print 'rename result=', ret
            print 'rename %s to %s' % (src, dest)
        else:
            print "%s not changed" % src
