#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2019-12-13

# depends on exifread, click
import os
import sys
import shutil
import click
import logging
from os import path
from datetime import datetime
from lib_exif import get_date_time
# from PIL import Image
# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3

# logging.basicConfig(level=logging.INFO)


def get_full_class_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__


def get_log_filename():
    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    return '/tmp/rename_{}.log'.format(dt)


def create_logger():
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
    #                     datefmt='%H:%M:%S',
    #                     filename=get_log_filename(),
    #                     filemode='a')
    # logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s][%(name)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S')

    fsh = logging.FileHandler(filename=get_log_filename())
    fsh.setFormatter(formatter)
    fsh.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)

    logger = logging.getLogger("EXIF")
    logger.addHandler(fsh)
    logger.addHandler(console)

    return logger


logger = create_logger()

EXIF_DATE_TIME = '%Y:%m:%d %H:%M:%S'
NAME_DATE_TIME = 'IMG_%Y%m%d_%H%M%S'
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')


def valid_image(root, name, real):
    src_path = path.normpath(path.join(root, name))
    base, ext = path.splitext(name)
    if name.startswith(".") or name.startswith("_"):
        logger.warning("Remove invalid file: {}".format(src_path))
        if real:
            os.remove(src_path)
        return False
    if path.getsize(src_path) < 10*1024:
        logger.info("Remove small file: {}".format(src_path))
        if real:
            os.remove(src_path)
        return False
    if not (ext and ext.lower() in IMAGE_EXTENSIONS):
        logger.info("Not image: {}".format(src_path))
        return False
    return True


def get_dst_path(src_path, real):
    root = path.dirname(src_path)
    name = path.basename(src_path)
    base, ext = path.splitext(name)
    exif_date_time = get_date_time(src_path)
    if not exif_date_time:
        logger.info("No Exif: {}".format(src_path))
        return
    name_str_prefix = datetime.strftime(exif_date_time, NAME_DATE_TIME)
    if name_str_prefix.lower() == base.lower() or name_str_prefix.lower().startswith(base.lower()):
        logger.info('No need rename: %s' % src_path)
        return
    ### handle duplicate file start ###
    dup_count = 0
    name_str = name_str_prefix
    while path.exists(path.join(root, name_str+ext)):
        name_str = '{}_{}'.format(name_str_prefix, dup_count)
        new_dst_path = path.join(root, name_str+ext)
        # same file: equal name + equal size
        if path.exists(new_dst_path) and (path.getsize(new_dst_path) == path.getsize(src_path)):
            logger.debug(
                'Duplicate found: {}->{}'.format(src_path, new_dst_path))
            return
        dup_count += 1
    ### handle duplicate file end ###
    dst_path = path.join(root, name_str+ext)
    if dup_count > 0:
        logger.warning('Handle duplicate: {}->{}'.format
                       (src_path, dst_path))
    if path.exists(dst_path):
        logger.warning('Skip exists: %s' % src_path)
        return
    return dst_path


def list_images(target, real):
    files = []
    top = path.abspath(path.normpath(target))
    for root, dirs, names in os.walk(top):
        for name in names:
            src_path = path.normpath(path.join(root, name))
            if valid_image(root, name, real):
                files.append(src_path)
    return files


@click.command()
@click.option('-r', '--real', default=False, show_default=True, is_flag=True,
              help='Execute command in real mode')
@click.argument('source', required=True, type=click.Path(exists=True, resolve_path=True, dir_okay=True, file_okay=False))
def exif_rename(source, real=False):
    '''Using exif date time to rename all images in source directory.'''
    top = path.abspath(path.normpath(source))
    logger.info('Source:{} (Real:{})'.format(top, real))
    count = 0
    files = list_images(source, real)
    logger.info('Total files count: {}'.format(len(files)))
    for src_path in files:
        count += 1
        logger.debug("Processing: {} ({})".format(src_path, count))
        dst_path = get_dst_path(src_path, real)
        if not dst_path:
            continue
        logger.info('Renamed to {} ({}) ({})'.format(
            dst_path, count, real))
        if real:
            os.rename(src_path, dst_path)


if __name__ == '__main__':
    exif_rename()
