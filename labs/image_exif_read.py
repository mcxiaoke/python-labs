#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-10 08:24:23

import os
import sys
import exifread
from os import path

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

if len(sys.argv) < 2:
    print 'Usage: python %s some_directory' % sys.argv[0]
    sys.exit(1)

top = path.normcase(sys.argv[1])
log = open(path.join(top, 'log.txt'), 'w')
for root, dirs, files in os.walk(top):
    for name in files:
        _, ext = path.splitext(name)
        print ext
        if not ext or ext.lower() not in ['.jpg', '.png']:
            continue
        print "process file: ", path.abspath(name)
        f = open(path.join(root, name), 'rb')
        tags = exifread.process_file(f)
        f.close()
        log.write("File: %s\n" % path.basename(name))
        for tag in tags:
            if tag in TAGS:
                log.write('\t%s=%s\n' % (tag.split()[1], tags[tag]))

log.close()
