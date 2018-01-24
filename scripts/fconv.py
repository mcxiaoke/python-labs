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

RE_URL = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

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
            encoding = ct['encoding']
        else:
            encoding = UnicodeDammit(data).original_encoding
        encoding = fix_encoding(encoding)
        utf8_data = to_text(data, encoding=encoding)
        print('convert_to_utf8() encoding:%s file:%s' % (encoding, src))
        with codecs.open(dst, 'w', 'utf-8') as fw:
            fw.write(utf8_data)


def smart_convert():
    arg = upath.abspath(sys.argv[1])
    if upath.isfile(arg):
        convert_to_utf8(arg)
    else:
        for name in upath.listdir(arg):
            convert_to_utf8(os.path.join(arg, name), override=True)


def enca_convert():
    root = upath.abspath(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] == '-z':
        dry_run = False
    else:
        dry_run = True
    log = codecs.open('../enca.log', 'w', 'utf-8')
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            try:
                f = os.path.join(curdir, name)
                if dry_run:
                    cmd = ['enca', f]
                else:
                    cmd = 'iconv -f GB18030 -t UTF-8 -c'.split()
                    cmd.append(f)
                print(cmd)
                r = subprocess.check_output(cmd)
                r = compat.to_text(r)
                print('%s - %s' % (f, r))
            except Exception as e:
                traceback.print_exc()
                log.write(f)


def manual_convert():
    root = upath.abspath(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] == '--convert':
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
    if len(sys.argv) == 3 and sys.argv[2] == '-z':
        dry_run = False
    else:
        dry_run = True
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
                    while not new_name or len(new_name) > 25:
                        new_name = f.readline().strip()
                new_name = new_name.replace('标  题: ', '')
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


def move_from_subdirs():
    root = upath.abspath(sys.argv[1])
    if len(sys.argv) == 3 and sys.argv[2] == '-z':
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


def move_some_files():
    root = upath.abspath(sys.argv[1])
    output = upath.abspath(sys.argv[2])
    dry_run = not (len(sys.argv) == 4 and sys.argv[3] == '-z')
    if not os.path.exists(output):
        os.makedirs(output)
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            src = os.path.join(curdir, name)
            dst = os.path.join(output, name)
            # print('Processing %s' % src)
            if not os.path.isfile(src):
                continue
            if src == dst:
                continue
            file_size = os.path.getsize(src)
            if file_size < 30000:
                if not dry_run:
                    print('Moving %s %s size=%s' % (src, dst, file_size))
                    shutil.move(src, dst)

def move_noname_files():
    root = upath.abspath(sys.argv[1])
    output = upath.abspath(sys.argv[2])
    dry_run = not (len(sys.argv) == 4 and sys.argv[3] == '-z')
    if not os.path.exists(output):
        os.makedirs(output)
    p = re.compile(r'[a-zA-Z0-9]+\.txt')
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            src = os.path.join(curdir, name)
            dst = os.path.join(output, name)
            # print('Processing %s' % src)
            if not os.path.isfile(src):
                continue
            if src == dst:
                continue
            if re.match(p, name):
                if not dry_run:
                    print('Moving %s %s' % (src, dst))
                    shutil.move(src, dst)

def count_words(src):
    size = os.path.getsize(src)
    with codecs.open(src, 'r', 'utf8') as f:
        text = f.read()
        print('%s %s %s' % (src, len(text), size))

def remove_invalid_chars():
    root = upath.abspath(sys.argv[1])
    pattern = re.compile('[\u4E00-\u9FA5,.]+') # 中文
    invalid = re.compile('\uE4C6+') # \xee\x93\x86 U+E4C6 方块问号
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            src = os.path.join(curdir, name)
            if not os.path.isfile(src):
                continue
            _, ext = os.path.splitext(name)
            if not ext or ext.lower() != '.txt':
                continue
            with codecs.open(src, 'r', 'utf8') as f:
                content = f.read()
                content2 = content.replace('\uE4C6','')
            if len(content2) < len(content):
                print('Processing %s (%s %s)' % (src, len(content), len(content2)))
                with codecs.open(src, 'w', 'utf8') as f:
                    f.write(content2)

def move_by_pattern():
    root = upath.abspath(sys.argv[1])
    output = upath.abspath(sys.argv[2])
    re_str = compat.to_text(sys.argv[3])
    pattern = re.compile(re_str)
    dry_run = not (len(sys.argv) == 5 and sys.argv[4] == '-z')
    # output = os.path.join(output,re_str)
    if not os.path.exists(output):
        os.makedirs(output)
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            src = os.path.join(curdir, name)
            dst = os.path.join(output, name)
            # print('Processing %s' % src)
            if not os.path.isfile(src):
                continue
            if src == dst:
                continue
            if re.search(pattern, name):
                if not dry_run:
                    print('Moving %s %s' % (src, dst))
                    shutil.move(src, dst)
                else:
                    print('Demo %s %s' % (src, dst))

def remove_links():
    root = upath.abspath(sys.argv[1])
    p1 = re.compile(RE_URL)
    p2 = re.compile(r'[A-z0-9]+\.[A-z0-9]+\.[A-z0-9]+')
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        for name in filenames:
            src = os.path.join(curdir, name)
            if not os.path.isfile(src):
                continue
            _, ext = os.path.splitext(name)
            if not ext or ext.lower() != '.txt':
                continue
            with codecs.open(src, 'r', 'utf8') as f:
                content = f.read()
                content2 = re.sub(p2, '', content)
            if len(content2) < len(content):
                print('Processing %s (%s %s)' % (src, len(content), len(content2)))
                with codecs.open(src, 'w', 'utf8') as f:
                    f.write(content2)

def main():
    # first_line_as_title()
    # move_noname_files()
    # remove_links()
    # remove_invalid_chars()
    # move_some_files()
    move_by_pattern()
    # move_from_subdirs()
    # first_line_as_title()
    # enca_convert()
    # manual_convert()


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat, upath
    main()
