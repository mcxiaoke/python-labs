#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2017-05-26 20:30:00

from __future__ import print_function
import os
import sys
import shutil
import re
import time
from datetime import datetime

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

# compat 2.x and 3.x

try:
    input = raw_input
except Exception:
    pass

os_encoding = sys.getfilesystemencoding()
os_win = sys.platform.startswith('win')

# print(sys.version_info)
# print(sys.platform, sys.stdin.encoding, sys.stdout.encoding, os_encoding)

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
DATE_FORMAT = '%Y%m%d'
EXIF_DATE_TIME = '%Y:%m:%d %H:%M:%S'

def bad_filename(s):
    return repr(s)[1:-1]

def fix_print(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(bad_filename(s))

def copy_by_date(source, destination, since, max_depth=5):
    if not source or not destination or not since:
        return -1
    if PY2:
        source = source.decode(os_encoding)
        destination = destination.decode(os_encoding)
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)
    since = datetime.strptime(since, DATE_FORMAT)
    log(u'SRC:  {}'.format(source))
    log(u'DST:  {}'.format(destination))
    log(u'DATE:  {}'.format(since))
    if not os.path.exists(destination):
        os.makedirs(destination)
    copied_count = 0
    for root, dirs, files in os.walk(source, topdown=True):
        level = root.replace(source, '').count(os.sep)
        if level >= max_depth:
            continue
        for name in files:
            src = os.path.join(root, name)
            log(u'Processing {}'.format(src))
            if name[0] in '._~':
                log(u'Invalid: {}'.format(src))
                continue
            if os.path.getsize(src) < IMG_FILE_MIN_SIZE:
                log(u'Invalid: {}'.format(src))
                continue
            t = time.ctime(os.path.getmtime(src))
            t = datetime.strptime(t, "%a %b %d %H:%M:%S %Y")
            if t < since:
                dst = os.path.join(destination, name)
                if not os.path.exists(dst):
                    log(u'Copying {} -> {}'.format(src, dst))
                    shutil.copy2(src, dst)
                    copied_count += 1
                else:
                    log(u'Exist: {}'.format(dst))
    log(u'Result: %s files copied!' % copied_count)
    return copied_count

def backup(source, destination, dry_run=False):
    if PY2:
        source = source.decode(os_encoding)
        destination = destination.decode(os_encoding)
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)
    log(u'SRC:  {}'.format(source))
    log(u'DST:  {}'.format(destination))
    if dry_run:
        log(u"Mode: dry run mode, no files will be copied.")
    ip = re.compile(IMG_NAME_PATTERN, re.I)
    log(u'Processing: {}'.format(source))
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
    copy_by_date(sys.argv[1],sys.argv[2], sys.argv[3])
    # fire.Fire(backup)
