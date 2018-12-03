#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-10 08:24:23

from __future__ import print_function
import os
import sys
import shutil
import codecs
import exifread
from os import path
from datetime import datetime

EXIF_DATE_TIME = '%Y:%m:%d %H:%M:%S'
NAME_DATE_TIME = 'IMG_%Y%m%d_%H%M%S'

def move_to_sub(src_path):
    src_dir, src_name = path.split(src_path)
    dst_dir = path.join(src_dir, 'noexif')
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    print('Move %s to %s' % (src_name, dst_dir))
    shutil.move(src_path, dst_dir)

def move_no_exif(top_dir, dry_run=True):
    top = path.normcase(top_dir)
    count = 0
    for root, dirs, files in os.walk(top):
        if 'noexif' in dirs:
            dirs.remove('noexif')
        for name in files:
            base, ext = path.splitext(name)
            if not ext or ext.lower() not in ['.jpg', '.tiff']:
                continue
            if name.startswith('IMG_'):
                continue
            rel_path = path.join(root, name)
            src_path = path.abspath(rel_path)
            # print("Processing: %s" % src_path)
            f = open(path.join(root, name), 'rb')
            tags = exifread.process_file(f)
            f.close()
            if not tags:
                # print('No exif tags found: %s' % name)
                move_to_sub(src_path)
                continue
            exif_d1 = tags.get('EXIF DateTimeDigitized')
            exif_d2 = tags.get('EXIF DateTimeOriginal')
            exif_d3 = tags.get('Image DateTime')
            exif_date_time_obj = exif_d1 or exif_d2 or exif_d3
            if not exif_date_time_obj:
                # print("Exif date not found, skip %s" % name)
                move_to_sub(src_path)
                continue
            try:
                exif_date_time_str = str(exif_date_time_obj)
                exif_date_time = datetime.strptime(
                    exif_date_time_str, EXIF_DATE_TIME)
            except:
                # print("Invalid exif date:  %s" % name)
                move_to_sub(src_path)
                continue
            if not exif_date_time:
                # print("Exif date not found, skip %s" % name)
                move_to_sub(src_path)
                continue


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 2:
        # default dry run mode, -e for real mode
        print('Usage: python %s some_directory' % sys.argv[0])
        sys.exit(1)
    top_dir = sys.argv[1]
    dry_run = len(sys.argv) < 3 or sys.argv[2] != '-e'
    move_no_exif(top_dir, dry_run)
