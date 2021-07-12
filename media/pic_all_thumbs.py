#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2020-10-04 22:29:40
import os
import time
from os import path
import pathlib
from datetime import datetime
import sys
import shutil
import signal
import re
from PIL import Image
from multiprocessing.dummy import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from threading import currentThread
from lib_exif import is_normal_image

# Generating thumbs for all images in a folder
# 给某一个目录及子目录的全部图片生成缩略图
# 缩略图放入单独的相机小图目录

MAX_WIDTH = 3000  # (6000x4000 -> 3000x2000)


def get_year():
    return str(datetime.now().year)


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
    file_name = path.basename(src)
    fbase, ext = path.splitext(file_name)
    return '{}_thumb{}'.format(fbase, ext)


def make_thumb_one(src, dst, index=0):
    max_width = MAX_WIDTH
    file_name = path.basename(src)
    fbase, ext = path.splitext(file_name)
    # print("{},{},{}".format(src, dst, file_name))
    if not is_normal_image(src):
        print("Not image: {}".format(dst))
        return
    if not path.exists(dst):
        try:
            os.makedirs(dst, exist_ok=True)
        except:
            pass
    dst = path.join(dst, get_thumb_filename(src))
    dst = path.abspath(dst)
    if not path.exists(src):
        print("Not exists: {}".format(src))
        return
    if path.exists(dst):
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
            nim.save(dst, format='JPEG', quality=85, exif=im.info['exif'])
            print("[{}] DST: {} {} ({}-{})".format(index,
                                                   dst, nim.size, os.getpid(), currentThread().name))
            return dst
    except Exception as e:
        print(e)


def make_thumb_one_args(args):
    return make_thumb_one(args[0], args[1], args[2])


def make_thumbs(src_dir):
    src_dir = path.abspath(src_dir)
    print('Root:{}'.format(src_dir))
    # if '相机照片' not in src_dir and 'JPEG' not in src_dir:
    #     print('Invalid Path:{}'.format(src_dir))
    #     return
    index = 0
    images = []
    dst_dir = ''
    for root, dirs, files in os.walk(src_dir):
        dn = root.lower()
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
        print('Searching... in', path.abspath(root))
        path_replace = path.join('Thumbs', get_year(), '相机小图')
        for name in files:
            if 'thumb' in name.lower():
                continue
            src_path = path.abspath(path.join(root, name))
            if not is_normal_image(src_path):
                continue
            if '相机照片' in root:
                dst_path = path.abspath(root).replace(
                    '相机照片', path_replace)
            elif 'JPEG' in root:
                dst_path = path.abspath(root).replace(
                    'JPEG', path_replace)
                print(dst_path)
            elif 'Temp' in root:
                dst_path = path.abspath(root).replace(
                    'Temp', path_replace)
            else:
                dst_root = path.expanduser('~/Pictures/'+path_replace)
                dst_path = path.join(dst_root, root)
            dst_file = path.join(dst_path, get_thumb_filename(src_path))
            if path.exists(dst_file):
                # print("Skip: {}".format(dst_file))
                continue
            index = index + 1
            images.append((src_path, dst_path, index))
            # print("New Thumb: {}".format(dst_file))
    total = len(images)
    if total > 0:
        dst_dir = images[0][1]
    print('Images: {}'.format(src_dir))
    print('Thumbs: {}'.format(dst_dir))
    print('{} images will be processed.'.format(total))
    sel = input("Press Enter yes/y to continue: ")
    if not sel.startswith("y"):
        print("Aborted.")
        return
    start = time.time()
    with ProcessPoolExecutor(max_workers=os.cpu_count()-1) as executor:
        futures = {executor.submit(
            make_thumb_one_args, img): img for img in images}
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                print(e)
    # with Pool(os.cpu_count()) as p:
    #     p.map_async(make_thumb_one_args, images)
    #     p.close()
    #     p.join()
    # p = Pool(os.cpu_count(),init_worker)
    # try:
    #      p.map_async(make_thumb_one_args, images)
    #      p.close()
    #      p.join()
    # except KeyboardInterrupt:
    #     print('Ctrl-C Aborted!')
    #     p.terminate()
    #     p.join()
    # Ctrl-C Ctrl-Break to quit program
    # https://stackoverflow.com/questions/42039231
    elapsed = time.time()-start
    print("Task finished, {} files, using {} seconds.".format(total, elapsed))


if __name__ == '__main__':
    make_thumbs(sys.argv[1])
