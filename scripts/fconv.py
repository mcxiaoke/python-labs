#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import, print_function
import os
import sys
import re
import codecs
import shutil
import chardet
import traceback
import subprocess
from bs4 import UnicodeDammit

'''
#shell version
find ./ -name "*.txt" -o -name "*.html" -type f |
while read file
do
  echo " $file"
  mv $file $file.tmp
  iconv -c -f $1 -t UTF-8 $file.tmp > $file
  rm -f $file.icv
done
'''

sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))

from lib.compat import to_text, text_type, binary_type
from lib import upath

CN_ENCODING_LIST = ['windows-1252', 'gb2312', 'gbk']

def fix_encoding(encoding):
    if encoding.lower() in CN_ENCODING_LIST:
        return 'gb18030'
    else:
        return encoding

def convert_to_utf8(src, output=None, override=False):
    src = upath.abspath(src)
    print(src)
    filename = os.path.basename(src)
    output = upath.abspath(output) if output else None
    dir_ = upath.abspath(os.path.dirname(src))
    if override:
        dst = src
    else:
        if dir_ == output:
            dst = os.path.join(output, filename)
        else:
            dst = os.path.join(output or dir_, '_%s' % filename)
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    
    with open(src, 'rb') as fr:
        data = fr.read()
        ct = chardet.detect(data)
        if ct['confidence'] > 0.90:
            encoding=ct['encoding']
        else:
            encoding = UnicodeDammit(data).original_encoding
        encoding = fix_encoding(encoding)
        utf8_data = to_text(data, encoding=encoding)
        print('convert_to_utf8() encoding:%s file:%s' %(encoding, src))
        with codecs.open(dst, 'w', 'utf-8') as fw:
            fw.write(utf8_data)

def smart_convert():
    arg = upath.abspath(sys.argv[1])
    if upath.isfile(arg):
        convert_to_utf8(arg)
    else:
        for name in upath.listdir(arg):
            convert_to_utf8(os.path.join(arg,name), override=True)

def enca_convert():
    root = upath.abspath(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] =='--convert':
        dry_run = False
    else:
        dry_run = True
    log = codecs.open('../enca.log', 'w', 'utf-8')
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            try:
                f = os.path.join(curdir,name)
                if dry_run:
                    cmd = ['enca', f]
                else:
                    cmd = 'iconv -f GB18030 -t UTF-8 -c'.split()
                    cmd.append(f)
                print(cmd)
                r = subprocess.check_output(cmd)
                r = compat.to_text(r)
                print('%s - %s' % (f,r))
            except Exception as e:
                traceback.print_exc()
                log.write(f)

def manual_convert():
    root = upath.abspath(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] =='--convert':
        dry_run = False
    else:
        dry_run = True
    log = codecs.open('../convert.log', 'w', 'utf-8')
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            try:
                src = os.path.join(curdir, name)
                print('Converting %s' % src)
                with open(src, 'rb') as f:
                    data = f.read()
                dst = src
                if dry_run:
                    dst = os.path.join(curdir, '_%s' % name)
                else:
                    dst = src
                utf8_data = compat.to_text(data, encoding='gb18030')
                with codecs.open(dst, 'w', 'utf-8') as f:
                    f.write(utf8_data)
            except Exception as e:
                traceback.print_exc()
                log.write(src)

def first_line_as_title():
    root = upath.abspath(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] =='--convert':
        dry_run = False
    else:
        dry_run = True
    log = codecs.open('../fix_title.log', 'w', 'utf-8')
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            src = os.path.join(curdir, name)
            if not os.path.isfile(src):
                continue
            print('Fix %s' % src)
            try:
                new_name = None
                with codecs.open(src, 'r', 'utf-8') as f:
                    new_name = f.readline().strip()
                    # while ':' in new_name:
                        # new_name = f.readline().strip()
                        # new_name = new_name.replace('标 题:','')
                if new_name and new_name != name:
                    print('New name: %s' % new_name)
                    if not dry_run:
                        dst = os.path.join(curdir, '%s.txt' % new_name)
                        shutil.move(src, dst)
                        print('Rename to: %s' % dst)
                else:
                    print('Skip %s' % src)
            except Exception as e:
                traceback.print_exc()
                log.write(src)

def move_from_subdirs():
    root = upath.abspath(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] =='--move':
        dry_run = False
    else:
        dry_run = True
    log = codecs.open('../fix_title.log', 'w', 'utf-8')
    print(root)
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        if curdir == root:
            continue
        for name in filenames:
            src = os.path.join(curdir, name)
            if not os.path.isfile(src):
                continue
            dst = os.path.join(root, name)
            print('File %s -> %s' % (src, dst))
            try:
                if not dry_run:
                    shutil.move(src, dst)
                    print('Move %s -> %s' % (src, dst))
            except Exception as e:
                traceback.print_exc()
                log.write(src)

def move_by_pattern():
    pat_str = compat.to_text(sys.argv[2])
    pattern = re.compile('.*%s.*' % pat_str, re.I)
    print(pattern)
    root = upath.abspath(sys.argv[1])
    output = os.path.join(root, pat_str)
    if not os.path.exists(output):
        os.mkdir(output)
    for name in os.listdir(root):
        if re.search(pattern, name):
            src = os.path.join(root, name)
            dst = os.path.join(output, name)
            if os.path.isfile(src) and src != dst:
                print('Move %s %s' % (src, dst))
                shutil.move(src, dst)
        

def main():
    # move_by_pattern()
    move_from_subdirs()
    # first_line_as_title()
    # enca_convert()
    # manual_convert()

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat, upath
    main()

