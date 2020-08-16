#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-12-11 17:03:40
import os
import time
from os import path
import sys
import shutil
import re
from PIL import Image
from multiprocessing.dummy import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from threading import currentThread

MAX_WIDTH = 3600  # (6000x4000 -> 3600x2400)
EXTENSIONS = ('.jpg', '.png', '.gif', '.tiff')


def resize_one(src, dst, max_width):
    _, ext = os.path.splitext(os.path.basename(src))
    if not ext or ext.lower() not in EXTENSIONS:
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


def clear_thumbs(src_dir):
    for root, _, files in os.walk(src_dir):
        for name in files:
            if 'thumb' in name:
                os.remove(os.path.join(root, name))
                print('Remove thumb: {}'.format(os.path.join(root, name)))
    for root, dirs, _ in os.walk(src_dir):
        for adir in dirs:
            if 'thumb' in adir:
                os.rmdir(os.path.join(root, adir))
                print('Clear thumbs: {}'.format(os.path.join(root, adir)))


def get_thumb_filename(src):
    file_name = os.path.basename(src)
    fbase, ext = os.path.splitext(file_name)
    return '{}_thumb{}'.format(fbase, ext)


def make_thumb_one(src, dst, index=0):
    max_width = MAX_WIDTH
    file_name = os.path.basename(src)
    fbase, ext = os.path.splitext(file_name)
    # print("{},{},{}".format(src, dst, file_name))
    if not ext or ext.lower() not in EXTENSIONS:
        print("Not image: {}".format(dst))
        return
    dst = os.path.join(dst, get_thumb_filename(src))
    dst = os.path.abspath(dst)
    if not os.path.exists(src):
        print("Not exists: {}".format(src))
        return
    if os.path.exists(dst):
        print("Exists: {}".format(dst))
        return
    try:
        im = Image.open(src)
        width, height = im.size
        if width > max_width or height > max_width:
            # print("SRC: {} {}".format(src, im.size))
            if width > height:
                nw = max_width
                nh = int((float(height) * nw / float(width)))
            else:
                nh = max_width
                nw = int((float(width) * nh / float(height)))
            nim = im.resize((nw, nh))
            nim.save(dst, quality=85, exif=im.info['exif'])
            print("[{}] DST: {} {} ({},{})".format(index,
                                                   dst, nim.size, os.getpid(), currentThread().name))
            return dst
    except IOError as e:
        print(e)


def make_thumb_one_args(args):
    make_thumb_one(args[0], args[1], args[2])


def make_thumbs(root):
    index = 0
    images = []
    files = [f for f in os.listdir(
        root) if os.path.isfile(os.path.join(root, f))]
    for name in files:
        _, ext = path.splitext(name)
        if not ext or ext.lower() not in EXTENSIONS:
            continue
        src_file = path.abspath(path.join(root, name))
        dst_path = path.join(root, '精选小图')
        dst_file = path.join(dst_path, get_thumb_filename(src_file))
        if os.path.exists(dst_file):
            print("Skip: {}".format(dst_file))
            continue
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        index = index + 1
        images.append((src_file, dst_path, index))
        print("Prepare: {}".format(src_file))
    total = len(images)
    print('{} images will be processed.'.format(total))
    sel = input("Press Enter yes/y to continue: ")
    if not sel.startswith("y"):
        print("Aborted.")
        return
    start = time.time()
    with Pool(4) as p:
        p.map(make_thumb_one_args, images)
        p.close()
        p.join()
    elapsed = time.time()-start
    print("Task finished, {} files, using {} seconds.".format(total, elapsed))


if __name__ == '__main__':
    make_thumbs(sys.argv[1])
