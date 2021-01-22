#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2019-12-13

# depends on exifread, click
import os
import sys
import shutil
import time
from os import path
from datetime import datetime
import click
import click_log
import logging
from multiprocessing.dummy import Pool
# from loguru import logger
from lib_exif import IMG_FORMATS, RAW_FORMATS, EXIF_DATE_TIME, get_date_time, is_raw_image
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


'''
logger.add(
    sys.stderr, colorize=True, format="{time} {level} {message}", filter="", level="INFO")
logger.add("/tmp/exif_rename_{time}.log")
'''

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

IMG_NAME_DATE_TIME = 'IMG_%Y%m%d_%H%M%S'
RAW_NAME_DATE_TIME = 'DSC_%Y%m%d_%H%M%S'


def _short_path(p):
    return '/'.join(p.split('/')[-2:])


def valid_image(root, name):
    src_path = path.normpath(path.join(root, name))
    base, ext = path.splitext(name)
    if path.getsize(src_path) < 10*1024:
        logger.info("Remove small file: {}".format(_short_path(src_path)))
        return False
    if not ext:
        logger.info("No extension: {}".format(_short_path(src_path)))
        return False
    if ext.lower() in IMG_FORMATS or ext.lower() in RAW_FORMATS:
        return True
    logger.info("Not image: {}".format(_short_path(src_path)))
    return False


def get_dst_path(src_path, dst_path_list):
    root = path.dirname(src_path)
    name = path.basename(src_path)
    base, ext = path.splitext(name)
    short_path = _short_path(src_path)
    exif_date_time = get_date_time(src_path)
    if not exif_date_time:
        logger.warning("No Exif: {}".format(short_path))
        return
    name_format = RAW_NAME_DATE_TIME if is_raw_image(
        src_path) else IMG_NAME_DATE_TIME
    name_str_prefix = datetime.strftime(exif_date_time, name_format)
    if name_str_prefix.lower() == base.lower():
        logger.debug('Skip1: %s' % short_path)
        return
    if name.lower().startswith(name_str_prefix.lower()):
        logger.debug('Skip2: %s' % short_path)
        return
    ### handle duplicate file start ###
    dup_count = 0
    name_str = name_str_prefix
    while path.exists(path.join(root, name_str+ext)) or path.join(root, name_str+ext) in dst_path_list:
        name_str = '{}_{}'.format(name_str_prefix, dup_count)
        new_dst_path = path.join(root, name_str+ext)
        logger.debug('Duplicate name ,try next {}'.format(new_dst_path))
        dup_count += 1
    ### handle duplicate file end ###
    dst_path = path.join(root, name_str+ext)
    if dup_count > 0:
        logger.warning('New name: {}->{}'.format
                       (name, _short_path(dst_path)))
    if path.exists(dst_path):
        logger.debug('Skip exists: %s' % _short_path(dst_path))
        return
    return dst_path


def list_images(target):
    files = []
    top = path.abspath(path.normpath(target))
    for root, dirs, names in os.walk(top):
        for name in names:
            src_path = path.normpath(path.join(root, name))
            if valid_image(root, name):
                files.append(src_path)
    return sorted(files)


def exif_rename_one(args):
    print(args)
    src_path = args[0]
    dst_path = args[1]
    index = args[2]
    os.rename(src_path, dst_path)
    logger.info('Renamed({}): {} -> {}'.
                format(index, os.path.basename(src_path),
                       os.path.basename(dst_path)))


@click.command()
@click.option('-y', '--yes', default=False, show_default=False, is_flag=True,
              help='Execute command with no confirm')
@click.argument('source', required=True, type=click.Path(exists=True, resolve_path=True, dir_okay=True, file_okay=False))
@click_log.simple_verbosity_option(logger)
def exif_rename(source, yes=True):
    '''Using exif date time to rename all images in source directory.'''
    top = path.abspath(path.normpath(source))
    logger.info('Root:{} [yes:{}]'.format(top, yes))
    start = time.time()
    count = 0
    files = list_images(source)
    tasks = []
    dst_path_list = []
    for src_path in files:
        logger.debug('Processing: {}'.format(src_path))
        dst_path = get_dst_path(src_path, dst_path_list)
        if dst_path:
            count += 1
            dst_path_list.append(dst_path)
            tasks.append((src_path, dst_path, count))
            logger.info(
                'Add Task({}):{}->{}'.format(count, _short_path(src_path), _short_path(dst_path)))
    total = len(tasks)
    if total < 1:
        logger.info('Rename nothing.')
        return
    do_it = yes
    elapsed = time.time()-start
    logger.info('Processing {} files using seconds.'.format(
        total, elapsed/1000))
    if not do_it:
        logger.warning(
            '\nReady to rename {} files, Are you sure? yes/no'.format(total))
        answer = input()
        do_it = answer.startswith('y')
    else:
        logger.info('Now start to rename {} files.'.format(total))
    if do_it:
        for src_path, dst_path, index in tasks:
            os.rename(src_path, dst_path)
            logger.info('Renamed({}): {} -> {}'.
                        format(index, os.path.basename(src_path),
                               os.path.basename(dst_path)))
        logger.info("Tasks finished, {} files renamed.".format(
            total))
    else:
        for f, t in tasks:
            logger.debug('Ignored: {}->{}'.format(f, t))
        logger.warning('Aborted, nothing to do.')


if __name__ == '__main__':
    exif_rename()
