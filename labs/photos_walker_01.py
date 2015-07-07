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
# input:${input}/some_dir/xxxx.jpg
# output: ${output}/year/month/IMG_YYYYmmdd_HHMMSS.jpg
DIR_NAME_FORMAT = "%Y/%m"
FILE_NAME_FORMAT = "IMG_%Y%m%d_%H%M%S"
start_dir = path.abspath(sys.argv[1])
output_dir = path.join(path.dirname(start_dir), 'output')
if not path.exists(output_dir):
    os.mkdir(output_dir)
print 'start dir is %s' % start_dir
print 'output dir is %s' % output_dir

tasks = []


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
        dest_dir_name = fm.strftime(DIR_NAME_FORMAT)
        dest_dir = path.join(output_dir, dest_dir_name)
        src_path = path.abspath(path.join(dirname, src_name))
        dest_path = path.abspath(path.join(dest_dir, dest_name))
        if not path.exists(dest_dir):
            os.makedirs(dest_dir)
        print 'src is %s' % src_path
        print 'dest is %s' % dest_path
        tasks.append((src_path, dest_path))
    return 0


os.path.walk(start_dir, handler, ())
if tasks:
    for src, dest in tasks:
        if not path.exists(src):
            print "%s not exists." % src
        elif not path.isfile(src):
            print "%s is not file." % src
        elif path.exists(dest):
            print "%s already exists." % dest
        else:
            os.rename(src, dest)
            print 'move %s to %s' % (src, dest)
