#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2017-05-29 15:01:41
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2017-06-27 17:09:59
from __future__ import print_function
import sys
import os
import codecs
import re
import string
import shutil
from datetime import datetime

ISO_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FORMATS = ('.pdf', '.epub', '.mobi', '.azw3', '.djv', '.txt')
INVALID_CHARS = '~!@#$%^&*()+,._[]{}<>?`【】《》：”‘，。？'

processed = []


def log(x):
    print(x)


def _replace_invalid(s):
    for c in INVALID_CHARS:
        if c in s:
            s = s.replace(c, " ")
    s = s.replace('  ', ' ')
    s = s.replace('  ', ' ')
    return s.strip()


def nomalize_name(old_name):
    '''
    1. strip (xxx) at name start
        (Wiley Finance 019)Portfolio Theory and Performance Analysis.pdf
    2. strip 20_xxx at name start
        10_Novel Sensors for Food Inspection_Modelling,Fabrication and Experimentation 2014.pdf
        101 Ready-to-Use Excel Formulas-John Wiley & Sons(2014).pdf
        06.Head First Python.PDF
    3. strip press company name
        Addison-Wesley Starting Out with Visual Basic 2012 6th (2014).pdf
        ADDISON.WESLEY.DATA.JUST.RIGHT.2014.pdf
    4. repalce special chars and strip
        [] 【】 _
    5. capitalize characters
        04 - Seven Concurrency Models in Seven Weeks_When Threads (2014).epub
    '''
    # print('original: {}'.format(base))
    new_name = old_name
    # pass 1
    p = re.compile(r'(?:\(.+?\))\s*(.+)', re.I)
    m = p.match(old_name)
    if m:
        new_name = m.group(1)
        # print('pass1: {}'.format(new_base))
    # pass 2
    p = re.compile(r'\d+[-_\.](.+)', re.I)
    m = p.match(new_name)
    if m:
        new_name = m.group(1)
        # print('pass2: {}'.format(new_base))
    # pass 4
    new_name = _replace_invalid(new_name)
    # print('pass4: {}'.format(new_base))
    # pass 5
    # new_base = string.capwords(new_base)
    # print('pass5: {}'.format(new_base))
    return (old_name, new_name)


def fix_fileanme(old_path, dry_run=False):
    curdir = os.path.dirname(old_path)
    # log('file: {}'.format(old_path))
    old_name = os.path.basename(old_path)
    base, ext = os.path.splitext(old_name)
    if not ext:
        return old_path
    if ext.lower() not in FORMATS:
        return old_path
    # print(name)
    old_base, new_base = nomalize_name(base)
    if old_base == new_base:
        return old_path
    new_name = '{}{}'.format(new_base, ext.lower())
    new_path = os.path.join(curdir, new_name)
    # print(type(old_path), type(new_path))
    # print(repr(old_path)[1:-1])
    if not os.path.exists(old_path):
        log('Error: {}'.format(old_path))
        return old_path
    if new_path != old_path:
        if not os.path.exists(new_path):
            log('Rename: {} -> {}'.format(old_name, new_name))
            processed.append((old_path, new_path))
            if not dry_run:
                shutil.move(old_path, new_path)
                return new_path
        else:
            log('Exists: {}'.format(new_path))
    else:
        log('NoNeed: {}'.format(new_path))

    return old_path


def rename_ebooks(root, dry_run=False):
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        log('-- {} --'.format(curdir))
        for name in filenames:
            filename = os.path.join(curdir, name)
            fix_fileanme(filename, dry_run)
    logfile = os.path.join(root, 'logs.txt')
    log('processed count: {}'.format(len(processed)))
    with codecs.open(logfile, 'w', 'utf-8') as f:
        timestamp = datetime.strftime(datetime.now(), ISO_DATE_FORMAT)
        f.write('--- Time: {} ---\n'.format(timestamp))
        f.write('--- Root: {} ---\n'.format(root))
        if dry_run:
            f.write('--- Mode: dry run mode, no files will be renamed. ---\n')
        for (o, n) in processed:
            f.write('{} -> {}\n'.format(o, n))
        f.flush()


def contains_cjk(text):
    cjk_pattern = re.compile('[\u4e00-\u9fa5]+')
    return cjk_pattern.search(text)


def remove_cjk(root, dry_run=False):
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        log('-- {} --'.format(curdir))
        for name in filenames:
            if contains_cjk(name):
                log('Delete {}'.format(name))
                os.remove(os.path.join(curdir, name))


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    print(sys.argv)
    if len(sys.argv) < 2:
        log('Usage: {} target_dir -n'.format(sys.argv[0]))
        sys.exit(1)
    dry_run = False
    if len(sys.argv) == 3 and sys.argv[2] == '-n':
        dry_run = True
        log(u"Mode: dry run mode, no files will be renamed.")
    root = os.path.abspath(sys.argv[1])
    log('Root: {}'.format(root))
    rename_ebooks(root, dry_run)
