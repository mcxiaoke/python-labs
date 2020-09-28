#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-26 08:10:24
from __future__ import print_function
import os
import sys
import shutil


def get_files_by_name(top, name_str):
    result = []
    top = os.path.abspath(top)
    print('processing files in', top)
    for root, dirs, names in os.walk(top, topdown=True):
        dn = root.lower()
        if 'thumb' in dn:
            continue
        if '小图' in dn:
            continue
        if '精选' in dn:
            continue
        if 'feature' in dn:
            continue
        if 'web' in dn:
            continue
        print('Searching... in', root)
        files = [os.path.join(root, name) for name in names]
        result.extend(files)
    return [os.path.abspath(f) for f in result
            if name_str in f]


def rm_by_name(root, name_str):
    files = get_files_by_name(root, name_str)
    if not files:
        print('no file matched name "{0}" in {1}'.format(
            name_str, os.path.abspath(root)))
        return
    for f in files:
        print('found file:', f)
    confirm = input('Are you sure to remove all above files? [y/n]')
    if confirm.startswith('y'):
        for f in files:
            print('remove file:', f)
            os.remove(f)
    else:
        print('abort, no file deleted.')


if __name__ == '__main__':
    if len(sys.argv) != 3 or not sys.argv[1].strip():
        print('usage: {0} name str'.format(os.path.basename(sys.argv[0])))
        sys.exit()
    else:
        root = sys.argv[1]
        name_str = sys.argv[2]
        rm_by_name(root, name_str)
