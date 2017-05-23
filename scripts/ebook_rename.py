# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2017-05-23 20:48:56
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2017-05-23 21:40:21
from __future__ import print_function
import os
import sys
from os import path

books = []

start_dir = '.'


def handler(arg, dirname, names):
    dir_path = path.join(dirname, dirname)
    print ("current dir is %s" % dir_path)
    for file in names:
        file_path = path.abspath(path.join(dirname, file))
        fpath, ext = path.splitext(file_path)
        dname = path.dirname(fpath)
        fname = path.basename(fpath)
        print("processing file: '%s' + '%s'" % (fname, ext))
        if ext:
            if ext.lower() in ['.pdf', '.epub', '.mobi', '.azw3']:
                books.append(file_path)
                print('store path to list: %s' % file_path)
            elif ext.lower() == '.txt':
                continue


def process():
    if books:
        for file in books:
            pass


def main():
    print(sys.argv)
    os.path.walk(sys.argv[1], handler, ())
    process()

if __name__ == '__main__':
    main()
