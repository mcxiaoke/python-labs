#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-10 14:13:05

import os
import sys
from os import path
import re
import tempfile
import shutil
import time

'''
    clean idea project files
    param: max_depth -> max depth for recursively, default=3
    param: permanently -> move to system tmp dir or permanently delete, default=False
'''


def clean(start_dir, max_depth=3, permanently=False):
    idea_pattern = re.compile(r'.*\.iml|build$|\.idea')
    deleted = []
    backup_dir_name = 'clean_idea_backup_%s' % str(time.time())
    backup_dir = path.join(tempfile.gettempdir(), backup_dir_name)
    for root, dirs, files in os.walk(start, topdown=True):
        for name in dirs:
            if name == '.git':
                dirs.remove(name)
        level = root.replace(start, '').count(os.sep)
        if level >= max_depth:
            continue
        for name in dirs+files:
            # print '--> %s' % path.join(root, name).replace(start,' ')
            if idea_pattern.match(name):
                # os.renames()
                file = path.join(root, name)
                deleted.append(file)
                if permanently:
                    if path.isfile(file):
                        os.remove(file)
                    else:
                        shutil.rmtree(file)
                else:
                    shutil.move(file, backup_dir)

                print("delete %s" % file)
    if deleted:
        print('cleaned in %s' % start)
        print('backup to %s' % backup_dir)
    else:
        print('no idea files in %s' % start)

if __name__ == '__main__':
    usage = ''''Usage: %s dir' Be careful, this script will
    remove all files and directories named .idea/*.iml/build
    ''' % path.basename(sys.argv[0])
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)
    start = '.'
    start = path.abspath(start)
    clean(start)
