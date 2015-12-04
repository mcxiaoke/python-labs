# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 2015/7/7 22:39.
__author__ = 'mcxiaoke'

import os, sys
from os import path

src_name = 'hello.txt'
src_dir = 'dir1'
dst_dir = 'dir3'
src = path.join(src_dir, src_name)
if not path.exists(src):
    print '%s not exists.' % path.abspath(src)
    sys.exit(1)
dst = path.join(dst_dir, src_name)
if path.exists(dst):
    print '%s already exists.' % path.abspath(dst)
    sys.exit(1)
if not path.exists(dst_dir):
    os.mkdir(dst_dir)
print src
print dst
os.rename(src, dst)
