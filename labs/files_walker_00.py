# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 2015/7/6 21:19.
__author__ = 'mcxiaoke'

import os, sys
from os import path

py_files = []

start_dir = '.'


def handler(arg, dirname, names):
    dir_path = path.join(dirname, dirname)
    print ("current dir is %s" % dir_path)
    for file in names:
        file_path = path.abspath(path.join(dirname, file))
        print "processing file: %s" % file_path
        root, ext = path.splitext(file_path)
        if ext:
            # 保存py文件路径到列表
            if ext.lower() == '.py':
                py_files.append(file_path)
                print 'store path to list: %s' % file_path
                # 删除扩展名为txt的文件
            elif ext.lower() == '.txt':
                os.remove(file_path)
                print 'delete unused txt file: %s' % file_path


os.path.walk(start_dir, handler, ())
if py_files:
    # 复制所有py文件到 ../output/目录
    target_dir = path.abspath('../output')
    # 如果目标目录不存在就创建
    if not path.exists(target_dir):
        os.mkdir(target_dir)
    print 'copy py files to %s' % target_dir
    for file in py_files:
        src = file
        # 目标文件名保持一致
        dest = path.join(target_dir, path.basename(src))
        if path.exists(src) and not path.exists(dest):
            pass
            # 如果源文件存在，且目标文件不存在则复制
            # open(dest, 'wb').write(open(src, 'rb').read())
            # print 'file copied to %s' % dest
        else:
            # 如果已存在，直接忽略
            print 'ignore exists file: %s' % dest
