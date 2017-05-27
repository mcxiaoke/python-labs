#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2017-05-26 20:30:00

from __future__ import print_function
import os
import sys
import shutil
import re

'''
match all these names:

DSC_20170516_213125.jpg
IMG_20170526_213125.jpg
20170526_213125.jpg
20160301_114104303_iOS.jpg
2015-11-23 001126.jpg
20170428_132844_005.jpg
20160301_013717000_iOS.png
'''

IMG_NAME_PATTERN = r'(?:[a-zA-Z]{1,4})?_?(20\d{2})[-_/]?(\d{2})[-_/]?(\d{2}).*\.(jpg|jpeg|gif|png|bmp|tiff)'
# 4(year)+2(month)+2(day)+4(ext) = 12
IMG_NAME_MIN_LEN = 12
IMG_FILE_MIN_SIZE = 10*1024


def backup(source, destination):
    ip = re.compile(IMG_NAME_PATTERN, re.I)
    print('process directory:', source)
    if not os.path.isdir(source):
        return
    for name in os.listdir(source):
        current = os.path.join(source, name)
        if name[0] in '._~':
            print('skip:', current)
            continue
        if os.path.isfile(current):
            # print('process file:', current)
            if len(name) < IMG_NAME_MIN_LEN:
                print('skip:', current)
                continue
            pic_size = os.stat(current).st_size
            if pic_size <= IMG_FILE_MIN_SIZE:
                print('skip:', current)
                # os.remove(current)
                continue
            m = ip.match(name)
            if m:
                # img, year, month, day, ext
                # print(m.group(1), m.group(2), m.group(
                #     3), m.group(4))
                src = current
                output = os.path.join(destination, m.group(1), m.group(2))
                if not os.path.exists(output):
                    os.makedirs(output)
                dst = os.path.join(output, name)
                print('from:', src)
                print('to:', dst)
                if not os.path.exists(dst):
                    # TODO copy file
                    # print('Copied -> {}'.format(dst.encode('utf8')))
                    # shutil.copy2(src,dst)
                    pass
                else:
                    print('exists:', dst)
            else:
                print('skip:', name)
        elif os.path.isdir(current):
            backup(current, destination)
        else:
            print('not directory:', current)

if __name__ == '__main__':
    # print(sys.argv)
    if len(sys.argv) != 3:
        print('Usage: {} source_dir destination_dir'.format(sys.argv[0]))
        sys.exit(1)
    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2])
    print('Source:\t\t{}'.format(src))
    print('Destination:\t{}'.format(dst))
    msg = "Are you sure to process files [y/n]? "
    if raw_input(msg).lower() not in ('y', 'yes'):
        sys.exit(2)
    backup(src, dst)
