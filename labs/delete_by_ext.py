#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-26 08:10:24
from __future__ import print_function
import os
import sys
import shutil


def get_files_by_extension(top, ext):
    result = []
    top = os.path.abspath(top)
    print('processing files in', top)
    for root, dirs, names in os.walk(top, topdown=True):
        # print('Searching... in', root)
        if '.git' in dirs:
            dirs.remove('.git')
        files = [os.path.join(root, name) for name in names]
        result.extend(files)
    return [os.path.abspath(f) for f in result
            if os.path.splitext(f)[-1] == ext]


def rm_by_ext(root, ext):
    files = get_files_by_extension(root, ext.replace('*', ''))
    if not files:
        print('no file matched "{0}" in {1}'.format(
            ext, os.path.abspath(root)))
        return
    for f in files:
        print('found file:', f)
    confirm = raw_input('Are you sure to remove all above files? [y/n]')
    if confirm == 'y':
        for f in files:
            print('remove file:', f)
            os.remove(f)
    else:
        print('abort, no file deleted.')

if __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        print('usage: {0} extension'.format(os.path.basename(sys.argv[0])))
        sys.exit()
    else:
        root = '.'
        ext = sys.argv[1]
        rm_by_ext(root, ext)
