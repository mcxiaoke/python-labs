#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2021-01-22


import exiftool
import sys
import os

src_file = sys.argv[1]
with exiftool.ExifTool() as et:
    d = et.get_metadata(src_file)
    print("{}".format(d["EXIF:DateTimeOriginal"]))
