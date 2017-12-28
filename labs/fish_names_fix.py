#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
from __future__ import print_function
import codecs
import os
import sys
import shutil
import re

# https://stackoverflow.com/questions/34015615/python-reversing-an-utf-8-string

fin = os.path.abspath(sys.argv[1])
fdir = os.path.dirname(fin)
name = os.path.basename(fin)
fixed_name = "fixed_{}".format(name)
fout = os.path.join(fdir,fixed_name)

li = set(open(fin).read().splitlines())
lt = sorted([l.decode('utf-8')[::-1] for l in li])
lo = [l[::-1] for l in lt]

print("Write to {}".format(fout))

with codecs.open(fout,'w','utf-8') as f:
    f.write('\n'.join(lo))
