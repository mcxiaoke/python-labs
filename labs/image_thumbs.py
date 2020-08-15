#!/usr/bin/env python
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

MAX_WIDTH = 2400  # (6000x4000 -> 2400x1600)
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
    if not ext or ext.lower() not in ['.jpg', '.png', '.gif']:
        print("Not image: {}".format(dst))
        return
    dst = os.path.join(dst, get_thumb_filename(src))
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
            nim.save(dst, quality=85)
            print("[{}] DST: {} {} ({},{})".format(index,
                                                   dst, nim.size, os.getpid(), currentThread().name))
            return dst
    except IOError as e:
        print(e)


def move_thumbs(src_dir):
    thumbs = []
    for root, dirs, files in os.walk(src_dir):
        for adir in dirs:
            if 'thumb' in adir:
                src = os.path.join(root, adir)
                dst = src.replace('/Photos/',
                                  '/Photos/Thumbs/')
                thumbs.append((src, dst))
                print(dst)
    for src, dst in thumbs:
        print('SRC: {}'.format(src))
        print('DST: {}'.format(dst))
        shutil.move(src, dst)


def make_thumb_one_args(args):
    make_thumb_one(args[0], args[1], args[2])


def make_thumbs(src_dir):
    index = 0
    images = []
    for root, dirs, files in os.walk(src_dir):
        for adir in dirs:
            dn = adir.lower()
            if 'thumb' in dn:
                continue
            if '小图' in dn:
                continue
            if '精选' in dn:
                continue
            if 'feature' in dn:
                continue
            if 'web' in dn:
                continue
        for name in files:
            if 'thumb' in name.lower():
                continue
            _, ext = path.splitext(name)
            if not ext or ext.lower() not in EXTENSIONS:
                continue
            src_path = path.abspath(path.join(root, name))
            # root_new = root.replace('/XWIN/Photos/', '/XWIN/Photos/Thumbs/')
            root_new = root.replace('/相机照片/', '/相机小图/')
            # dst_path = path.join(root_new, 'thumbs')
            dst_path = root_new
            dst_file = path.join(dst_path, get_thumb_filename(src_path))
            if os.path.exists(dst_file):
                print("Skip: {}".format(dst_file))
                continue
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            index = index + 1
            images.append((src_path, dst_path, index))
            print("Prepare: {}".format(src_path))
    total = len(images)
    print('{} images will be processed.'.format(total))
    sel = input("Press Enter yes/y to continue: ")
    if not sel.startswith("y"):
        print("Aborted.")
        return
    start = time.time()
    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     futures = {executor.submit(make_thumb_one, src, dst): (
    #         src, dst) for (src, dst) in images}
    #     for future in as_completed(futures):
    #         try:
    #             result = future.result()
    #         except Exception as e:
    #             print(e)
    with Pool(4) as p:
        # for (src, dst) in images:
            # print("Process:", src_path)
            # make_thumb_one(src, dst)
            # p.apply_async(make_thumb_one, (src, dst))
        p.map(make_thumb_one_args, images)
        p.close()
        p.join()
    elapsed = time.time()-start
    print("Task finished, {} files, using {} seconds.".format(total, elapsed))


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
    # move_thumbs(sys.argv[1])
    make_thumbs(sys.argv[1])
