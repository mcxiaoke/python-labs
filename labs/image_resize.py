#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-12-11 17:03:40
from __future__ import print_function
import os
import sys
import shutil
import re
from PIL import Image

MAX_WIDTH = 1600  # 1200 1600


def resize_one(src, dst, max_width):
    _, ext = os.path.splitext(os.path.basename(src))
    if not ext or ext.lower() not in ['.jpg', '.png', '.gif']:
        print("Not image: {}".format(dst))
        return
    _, ext = os.path.splitext(os.path.basename(dst))
    if not ext or ext.lower() != '.jpg':
        dst = "{}.jpg".format(dst)
    if not os.path.exists(src):
        print("Not exists: {}".format(src))
        return
    if os.path.exists(dst):
        print("Exists: {}".format(dst))
        return
    try:
        im = Image.open(src)
        width, height = im.size
        if width > max_width:
            print("SRC: {} {}".format(src, im.size))
            nw = max_width
            nh = int((float(height) * nw / float(width)))
            nim = im.resize((nw, nh))
            nim.save(dst, format='JPEG', quality=90)
            print("DST: {} {}".format(dst, nim.size))
            return dst
    except IOError as e:
        print(e)


def resize_batch(src, dst, max_width):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for name in sorted(os.listdir(src)):
        old_file = os.path.join(src, name)
        new_file = os.path.join(dst, name)
        resize_one(old_file, new_file, max_width)


def main():
    if len(sys.argv) < 2:
        print('Usage: python %s src [dst] [width]' % sys.argv[0])
        sys.exit(1)
    src = os.path.normcase(sys.argv[1])
    if not os.path.exists(src):
        print("Not exists: {}".format(src))
        sys.exit(2)
    max_width = MAX_WIDTH
    if len(sys.argv) >= 3:
        dst = os.path.normcase(sys.argv[2])
        if len(sys.argv) >= 4:
            max_width = int(sys.argv[3])
    else:
        d = os.path.dirname(src)
        n = os.path.basename(src)
        dst = os.path.join(d, "_{}".format(n))

    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    print("INPUT: {}".format(src))
    print("OUTPUT: {}".format(dst))
    print("MAX WIDTH: {}".format(max_width))

    if os.path.isfile(src):
        resize_one(src, dst, max_width)
    else:
        resize_batch(src, dst, max_width)


if __name__ == '__main__':
    main()
