# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-03-07 13:34:43
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2016-03-07 14:14:04
from __future__ import print_function, unicode_literals
import time
import sys
import os
import shutil

def main():
    files = os.listdir("output")
    for f in files:
        print(f)
        # shutil.move(os.path.join("files",f),os.path.join("files",ps[0]))

if __name__ == '__main__':
    main()
