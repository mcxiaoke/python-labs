#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2017-05-26 20:30:00

from __future__ import print_function
import os
import sys
import shutil
import re

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

# compat 2.x and 3.x

try:
    input = raw_input
except Exception:
    pass

os_encoding = sys.getfilesystemencoding()
os_win = sys.platform.startswith('win')

print(sys.version_info)
print(sys.platform, sys.stdin.encoding, sys.stdout.encoding, os_encoding)

# reload(sys)
# if os_win:
# sys.setdefaultencoding('utf-8')


def log(s):
    if os_win and PY2 and type(s) == str:
        print(s.decode('utf-8'))
    else:
        print(s)

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

IMG_NAME_PATTERN = r'(?:[a-zA-Z]{1,4})?_?(20\d{2})[-_/]?(\d{2})[-_/]?(\d{2}).*\.(\w{3})'
# 4(year)+2(month)+2(day)+4(ext) = 12
IMG_NAME_MIN_LEN = 12
IMG_FILE_MIN_SIZE = 10*1024


def bad_filename(s):
    return repr(s)[1:-1]


def fix_print(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(bad_filename(s))


def backup(source, destination, dry_run=False):
    ip = re.compile(IMG_NAME_PATTERN, re.I)
    log(u'Process: {}'.format(source))
    if not os.path.isdir(source):
        log(u'Not Directory: {}'.format(source))
        return
    for name in os.listdir(source):
        current = os.path.join(source, name)
        if name[0] in '._~':
            log(u'Invalid: {}'.format(current))
            continue
        if os.path.isfile(current):
            # log(u'Process file: {}'.format(current))
            if len(name) < IMG_NAME_MIN_LEN:
                log(u'Invalid:', current)
                continue
            pic_size = os.path.getsize(current)
            if pic_size < IMG_FILE_MIN_SIZE:
                log(u'Invalid: {}'.format(current))
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
                    log(u'Copy: {} -> {}'.format(src, dst))
                    if not dry_run:
                        shutil.copy2(src, dst)
                else:
                    log(u'Exist: {}'.format(dst))
            else:
                log(u'Not Matched: {}'.format(name))
        elif os.path.isdir(current):
            backup(current, destination, dry_run)
        else:
            log(u'Invalid: {}'.format(current))

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 3:
        print(u'Usage: {} source_dir destination_dir -n'.format(sys.argv[0]))
        sys.exit(1)
    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2])
    print(os.path.isdir(sys.argv[1]), os.path.isdir(sys.argv[2]))
    if PY2:
        src = src.decode(os_encoding)
        dst = dst.decode(os_encoding)
    log(u'SRC:  {}'.format(src))
    log(u'DST:  {}'.format(dst))
    dry_run = False
    if len(sys.argv) == 4 and sys.argv[3] == '-n':
        dry_run = True
        log(u"Mode: dry run mode, no files will be copied.")
    # else:
    #     msg = "Are you sure to process files [y/n]? "
    #     if input(msg).lower() not in ('y', 'yes'):
    #         log('Cancelled.')
    #         sys.exit(2)
    backup(src, dst, dry_run)
