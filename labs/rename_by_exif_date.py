#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-10 08:24:23
import os
import sys
import codecs
import exifread
from os import path
from datetime import datetime

TAGS = [
    'GPS GPSLatitude',
    'GPS GPSLongitude',
    'GPS GPSDate',
    'GPS GPSImgDirection',
    'Image DateTime',
    'Image Orientation',
    'Image Software',
    'Image Model',
    'Image Make',
    'Image XResolution',
    'Image YResolution',
    'EXIF ExifVersion',
    'EXIF ExifImageLength',
    'EXIF ExifImageWidth',
    'EXIF LensMake',
    'EXIF LensModel',
    'EXIF FocalLength',
    'EXIF WhiteBalance',
    'EXIF ISOSpeedRatings',
    'EXIF ExposureMode',
    'EXIF ExposureTime',
    'EXIF ExposureProgram',
    'EXIF DateTimeOriginal',
    'EXIF DateTimeDigitized',
]

NAME_TAGS = [
    'GPS GPSDate',
    'Image DateTime',
    'Image Model',
    'Image XResolution',
    'Image YResolution',
    'EXIF ExifImageLength',
    'EXIF ExifImageWidth',
    'EXIF ISOSpeedRatings',
    'EXIF DateTimeOriginal',
    'EXIF DateTimeDigitized',
]

EXIF_DATE_TIME = '%Y:%m:%d %H:%M:%S'
NAME_DATE_TIME = 'IMG_%Y%m%d_%H%M%S'


def exif_rename(top_dir, dry_run=True):
    top = path.normcase(top_dir)
    log = codecs.open('log.txt', 'w', 'utf-8')
    count = 0
    for root, dirs, files in os.walk(top):
        for name in files:
            base, ext = path.splitext(name)
            if not ext or ext.lower() not in ['.jpg', '.tiff']:
                continue
            rel_path = path.join(root, name)
            src_path = path.abspath(rel_path)
            # print("Processing: %s" % src_path)
            f = open(path.join(root, name), 'rb')
            tags = exifread.process_file(f)
            f.close()
            if not tags:
                print('No exif tags found: %s\n' % name)
                log.write('N:'+src_path+'\n')
                continue

            exif_d1 = tags.get('EXIF DateTimeDigitized')
            exif_d2 = tags.get('EXIF DateTimeOriginal')
            exif_d3 = tags.get('Image DateTime')
            exif_date_time_obj = exif_d1 or exif_d2 or exif_d3
            if not exif_date_time_obj:
                print("Exif date not found, skip %s" % name)
                log.write('I:'+src_path+'\n')
                continue
            # print("Exif date: %s" % exif_date_time_obj)
            try:
                exif_date_time_str = str(exif_date_time_obj)
                exif_date_time = datetime.strptime(
                    exif_date_time_str, EXIF_DATE_TIME)
            except:
                print("Invalid exif date:  %s" % name)
                log.write('D:'+src_path+'\n')
                continue
            if not exif_date_time:
                print("Exif date not found, skip %s" % name)
                log.write('T:'+src_path+'\n')
                continue
            name_str = datetime.strftime(exif_date_time, NAME_DATE_TIME)
            if name_str == base:
                # print('Skip exists %s' % dst_path)
                # log.write('E:'+src_path_u+'\n')
                continue

            ### remove duplicate file start ###
            dst_path = path.join(
                root, name_str+ext.lower())
            if path.exists(dst_path):
                count += 1
                if not dry_run:
                    if os.path.getsize(dst_path) == os.path.getsize(src_path):
                        os.remove(src_path)
                        print('[%s] Delete duplicate %s' % (count, src_path))
                else:
                    print('[DRY RUN %s] Delete duplicate %s' % (count, src_path))
                continue
            ### remove duplicate file end ###

            while path.exists(path.join(root, name_str+ext.lower())):
                name_str += 'x'
            dst_path = path.join(
                root, name_str+ext.lower())
            if path.exists(dst_path):
                # print('Skip exists %s' % src_path)
                # log.write('E:'+src_path_u+'\n')
                continue
            count += 1
            if not dry_run:
                os.rename(src_path, dst_path)
                print('[%s] Renamed to %s' % (count, dst_path))
            else:
                print('[DRY RUN %s] Renamed to %s' % (count, dst_path))
            log.flush()
    log.close()


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 2:
        # default dry run mode, -e for real mode
        print('Usage: python %s some_directory [-e]' % sys.argv[0])
        sys.exit(1)
    top_dir = sys.argv[1]
    dry_run = len(sys.argv) < 3 or sys.argv[2] != '-e'
    exif_rename(top_dir, dry_run)
