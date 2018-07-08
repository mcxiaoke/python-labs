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


class ImageInfo(object):

    def __init__(self, path, width, height, time=None, iso=0, model=None):
        self.path = path
        self.width = width
        self.height = height
        self.time = time
        self.iso = iso
        self.model = model

    def __str__(self):
        time_str = datetime.strftime(
            self.time, EXIF_DATE_TIME) if self.time else ''
        return 'Image{path=%s,width=%s,height=%s,time=%s,iso=%s,model=%s}' % (
            self.path, self.width, self.height,
            time_str, self.iso, self.model)

if len(sys.argv) < 2:
    print 'Usage: python %s some_directory' % sys.argv[0]
    sys.exit(1)

def main():
    top = unicode(path.normcase(sys.argv[1]))
    log = codecs.open(path.join(top, 'log.txt'), 'w', 'utf-8')
    for root, dirs, files in os.walk(top):
        for name in files:
            _, ext = path.splitext(name)
            if not ext or ext.lower() not in ['.jpg', '.png']:
                continue
            rel_path = path.join(root, name)
            src_path = path.abspath(rel_path)
            print "process file:", src_path
            f = open(path.join(root, name), 'rb')
            tags = exifread.process_file(f)
            f.close()
            if not tags:
                log.write('No exif tags found for: %s\n' % rel_path)
            
            img_path = src_path
            width_str = str(tags.get('EXIF ExifImageWidth'))
            height_str = str(tags.get('EXIF ExifImageLength'))
            img_w = int(width_str) if width_str and width_str.isdigit() else 0
            img_h = int(height_str) if height_str and height_str.isdigit() else 0
            exif_time = tags.get('Image DateTime')
            if not exif_time:
                print("exif date time not found, skip %s" % name)
                continue
            time_str = str(exif_time)
            img_time = datetime.strptime(time_str, EXIF_DATE_TIME)
            iso_str = str(tags.get('EXIF ISOSpeedRatings'))
            #print 'iso_str=%s' % iso_str
            img_iso = int(iso_str) if iso_str and iso_str.isdigit() else 0
            img_model = str(tags.get('Image Model'))
            img = ImageInfo(img_path, img_w, img_h, time=img_time,
                            iso=img_iso, model=img_model)
            exif_date_time_obj = tags.get('EXIF DateTimeDigitized')
            if not exif_date_time_obj:
                print("exif date time not found, skip %s" % name)
                continue
            exif_date_time_str = str(exif_date_time_obj)
            exif_date_time = datetime.strptime(
                exif_date_time_str, EXIF_DATE_TIME) if time_str else None
            if not exif_date_time:
                print("exif date time not found, skip %s" % name)
                continue
            dst_path = path.join(
                root, datetime.strftime(exif_date_time, NAME_DATE_TIME)+ext.lower())
            if path.exists(dst_path):
                print 'dst file exists, no need to rename, skip %s' % name
                continue
            os.rename(src_path, dst_path)
            print 'renamed to', dst_path
            log.flush()
    log.close()

if __name__ == '__main__':
    main()
