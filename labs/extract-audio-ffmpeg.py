# -*- coding: utf-8 -*-
# @Author: Miu
# @Date:   2017-06-27 21:41:37
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2017-06-27 22:24:32
from __future__ import print_function
import sys
import os
import codecs
import re
import string
import shutil
import subprocess
from os import path


def process(curdir, name):
    # subprocess.check_call(["ls", "-l"])
    # subprocess.check_output(["echo", "Hello World!"])
    base, ext = path.splitext(name)
    fi = path.join(curdir, name)
    fo = os.path.join(curdir, '{}.m4a'.format(base))
    print('input: {}'.format(fi))
    print('output: {}'.format(fo))
    # subprocess.call(["file", f])
    if name.lower().endswith('.mp4') and not os.path.exists(fo):
        args = "ffmpeg -i {} -vn -c:a copy {}".format(fi, fo).split()
        subprocess.call(args, stderr=subprocess.STDOUT)


def main(root):
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        print(u'-- {} --'.format(curdir))
        for name in filenames:
            process(curdir, name)

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 2:
        print('Usage: {} target_dir'.format(sys.argv[0]))
        sys.exit(1)
    root = os.path.abspath(sys.argv[1])
    print('Root: {}'.format(root))
    main(root)
