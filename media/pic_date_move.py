'''
File: pic_date_move.py
Created: 2021-04-01 10:46:38
Modified: 2021-04-01 10:46:43
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''

import os
import sys
import shutil
from datetime import date, datetime
import pathlib


def move_one_file(src_file):
    old_file = pathlib.Path(src_file)
    old_dir = pathlib.Path(old_file).parent
    name = old_file.name
    # old_file = pathlib.Path(old_dir, name)
    fd = datetime.fromtimestamp(old_file.stat().st_mtime)
    new_dir = pathlib.Path(old_dir.parent, fd.strftime('%Y%m%d'))
    new_file = pathlib.Path(new_dir, name)
    if not (new_dir.exists() and new_dir.samefile(old_dir)):
        if not new_dir.exists():
            new_dir.mkdir(parents=True, exist_ok=True)
        print('Move to', new_file)
        # old_file.rename(new_file)


def move_by_date(src_dir):
    '''
    move image files by file modified date 
    '''
    for root, _, files in os.walk(src_dir):
        print(root)
        for name in files:
            move_one_file(pathlib.Path(root, name))


move_by_date(sys.argv[1])
