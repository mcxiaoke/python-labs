# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-03-07 17:42:34
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2016-03-07 18:02:03
from __future__ import print_function
import codecs
import os
import sys
import requests
import shutil
import time


def main():
    root = sys.argv[1]
    to_ext = sys.argv[2]
    files = os.listdir(root)
    for f in files:
        src = os.path.join(root, f)
        if not os.path.isfile(src):
            continue
        t = '%s.%s' % (os.path.splitext(f)[0], to_ext)
        print('Rename %s -> %s' % (f, t))
        shutil.move(os.path.join(root, f), os.path.join(root, t))

if __name__ == '__main__':
    print(sys.argv)
    main()
