#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2017-05-26 20:30:00

from __future__ import print_function
import os
import sys
import shutil
import re

# compat 2.x and 3.x

try:
    input = raw_input
except Exception:
    pass

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


def backup(source, destination, dry_run=False):
    ip = re.compile(IMG_NAME_PATTERN, re.I)
    print('Process: {}'.format(source))
    if not os.path.isdir(source):
        return
    for name in os.listdir(source):
        current = os.path.join(source, name)
        if name[0] in '._~':
            print('Invalid: {}'.format(current))
            continue
        if os.path.isfile(current):
            # print('process file:', current)
            if len(name) < IMG_NAME_MIN_LEN:
                print('Invalid:', current)
                continue
            pic_size = os.stat(current).st_size
            if pic_size <= IMG_FILE_MIN_SIZE:
                print('Invalid: {}'.format(current))
                # os.remove(current)
                continue
            m = ip.match(name)
            if m:
                # year, month, day, ext
                # print(m.group(1), m.group(2), m.group(3))
                src = current
                output = os.path.join(destination, m.group(1), m.group(2))
                if not os.path.exists(output) and not dry_run:
                    os.makedirs(output)
                dst = os.path.join(output, name)
                if not os.path.exists(dst):
                    print('Copy: {} -> {}'.format(src, dst))
                    if not dry_run:
                        shutil.copy2(src, dst)
                else:
                    print('Exist: {}'.format(dst))
            else:
                print('Not Matched: {}'.format(name))
        elif os.path.isdir(current):
            backup(current, destination, dry_run)
        else:
            print('Invalid: {}'.format(current))

if __name__ == '__main__':
    # print(sys.argv)
    if len(sys.argv) < 3:
        print('Usage: {} source_dir destination_dir -n'.format(sys.argv[0]))
        sys.exit(1)
    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2])
    print('SRC:  {}'.format(src))
    print('DST:  {}'.format(dst))
    dry_run = False
    if len(sys.argv) == 4 and sys.argv[3] == '-n':
        dry_run = True
        print("Mode: dry run mode, no files will be copied.")
    # else:
    #     msg = "Are you sure to process files [y/n]? "
    #     if input(msg).lower() not in ('y', 'yes'):
    #         print('Cancelled.')
    #         sys.exit(2)
    backup(src, dst, dry_run)
