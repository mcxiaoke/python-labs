#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import codecs
import exifread
import shutil
from os import path
from datetime import datetime
from backup_photos_by_date import backup, copy_by_date

def move_by_name():
    SRC = u'/Volumes/BackupPlus/Backup/照片备份/手机照片/back'
    DST = u'/Volumes/BackupPlus/Backup/照片备份/手机照片/'
    backup(SRC, DST) 

def move_by_size(top_dir, dry_run=True):
    dst_dir = '/Volumes/BackupPlus/Backup/照片备份/手机照片/小图/'
    top = path.normcase(top_dir)
    log = codecs.open('log.txt', 'w', 'utf-8')
    for root, dirs, files in os.walk(top):
        for name in files:
            rel_path = path.join(root, name)
            src_path = path.abspath(rel_path)
            src_path_u = src_path.decode('utf-8')
            dst_path = os.path.join(dst_dir, name)
            if src_path == dst_path:
                continue
            # print("Processing: %s" % src_path)
            size = os.path.getsize(src_path)
            if name.lower().endswith('.jpg') and size < 1024 * 500:
                print("Move %s" % src_path)
                shutil.copy(src_path, dst_dir)
                os.remove(src_path)

def move_by_ext(top_dir, dry_run=True):
    dst_dir = '/Volumes/BackupPlus/Backup/照片备份/手机照片/截图/'
    top = path.normcase(top_dir)
    log = codecs.open('log.txt', 'w', 'utf-8')
    for root, dirs, files in os.walk(top):
        for name in files:
            rel_path = path.join(root, name)
            src_path = path.abspath(rel_path)
            src_path_u = src_path.decode('utf-8')
            dst_path = os.path.join(dst_dir, name)
            if src_path == dst_path:
                continue
            # print("Processing: %s" % rel_path)
            if name.lower().endswith('.png') and path.exists(src_path):
                shutil.move(src_path, dst_dir)
                # print("Copy: %s" % src_path)
                # shutil.copy(src_path, dst_dir)
                # os.rename(src_path, dst_path)
                # print('Delete: %s' % src_path)
                # os.remove(src_path)

if __name__ == '__main__':
    move_by_size(sys.argv[1])
    # move_by_name()



