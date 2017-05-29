# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2017-05-29 15:05:27
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2017-05-29 15:13:01
from __future__ import print_function
import re
import sys
import os

pattern = re.compile(u'.*[\u4e00-\u9fa5]+.*')

if __name__ == '__main__':
    root = os.path.abspath(sys.argv[1]).decode('utf-8')
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            m = pattern.match(name)
            if m:
                print(os.path.join(curdir, name))
