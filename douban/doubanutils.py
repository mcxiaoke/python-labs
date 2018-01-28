# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-16 13:40:26
# @Last Modified by:   mcxiaoke
from __future__ import print_function, unicode_literals, absolute_import
import codecs
import requests
import base64
import json
import sys
import os
import time
import shutil
import random
import argparse
import traceback
import pprint
import logging
from lxml import etree, html
from doubanapi import ApiClient
import doubanweb

sys.path.insert(1, os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))))
from lib.compat import urlparse
from lib.utils import (read_list, write_list, read_dict,
                       write_dict, write_file, read_file,
                       distinct_list, 
                       get_user_home, get_valid_filename)
from lib.commons import download_file, ThreadPoolExecutorStackTraced
from lib.structures import to_obj, to_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('doubanutils')

OUTPUT_ROOT = os.path.join('output', 'douban')
if not os.path.exists(OUTPUT_ROOT):
    os.makedirs(OUTPUT_ROOT)

executor = ThreadPoolExecutorStackTraced(max_workers=8)

token_file = os.path.join(get_user_home(), '.douban_token.dat')
api = ApiClient(token_file=token_file)


def _get_album_output(album):
    album_obj = to_obj(album)
    album_id = album_obj.id
    album_name = get_valid_filename(album_obj.title)
    return os.path.join(OUTPUT_ROOT, 'albums', '%s_%s' % (album_name, album_id))


def _get_doulist_output():
    return os.path.join(OUTPUT_ROOT, 'doulist')


def _get_user_output():
    return os.path.join(OUTPUT_ROOT, 'user')


def _compat_album_id(param):
    # compat for param is album url
    if '/photos/album/' in param:
        album_id = doubanweb.get_id_from_album_url(param)
    else:
        return param


def _compat_doulist_id(param):
    # compat for param is doulist url
    if '/doulist/' in param:
        album_id = doubanweb.get_id_from_doulist_url(param)
    else:
        return param


def upload_photos_to_album(album_id, photos):
    album_id = _compat_album_id(album_id)
    logger.info('upload_photos_to_album %s' % album_id)
    if os.path.isfile(photos):
        files = [os.path.basename(photos)]
        output = os.path.dirname(photos)
    else:
        files = os.listdir(photos)
        output = photos
    done_file = os.path.join(output, '%s_done.txt' % album_id)
    finished = read_list(done_file)
    error_count = 0
    for f in files:
        image = os.path.join(output, f)
        _, ext = os.path.splitext(f)
        if not ext or ext.lower() not in ['.jpg', '.png', '.gif']:
            # print('Invalid %s' % image)
            continue
        try:
            if f not in finished:
                logger.info('upload_photos_to_album uploading %s' % image)
                api.photo_upload(album_id, image, f)
                finished.append(f)
                write_list(done_file, finished)
                time.sleep(random.randint(1, 3))
            else:
                print('Skip %s' % image)
        except KeyboardInterrupt as e:
            logger.warning("upload_photos_to_album user interrupt, quit.")
            raise
        except Exception as e:
            logger.warning(
                "upload_photos_to_album error:%s on uploading :%s" % (e, image))
            traceback.print_exc()
            error_count += 1
            if error_count > 5:
                break
            time.sleep(error_count * 10)
    write_list(done_file, finished)


def _fetch_album_photos(album_id):
    album_id = _compat_album_id(album_id)
    logger.info('fetch_album_photos album %s' % album_id)
    data = None
    photos = []
    count = doubanweb.COUNT
    while True:
        data = api.album_photos(album_id, start=len(photos), count=count)
        new_photos = data['photos']
        if not new_photos:
            break
        logger.info('fetch_album_photos %s new photos found in %s'
                    % (len(new_photos), album_id))
        # new_urls = [p.get('large') or p.get('image') for p in photos]
        photos.extend(new_photos)
        if len(photos) < count / 2:
            break
    logger.info('fetch_album_photos %s photos found in %s'
                % (len(photos), album_id))
    data['photos'] = photos
    return data


def get_album_photos(album_id):
    # https://api.douban.com/v2/album/1622166069/photos
    album_id = _compat_album_id(album_id)
    logger.info('get_album_photos %s' % album_id)
    data_file = os.path.join(OUTPUT_ROOT, 'album_photos_%s.dat' % album_id)
    if os.path.exists(data_file):
        data = read_dict(data_file)
        logger.info('get_album_photos read %s' % album_id)
    else:
        data = _fetch_album_photos(album_id)
        logger.info('get_album_photos fetch %s' % album_id)
        if data:
            write_dict(data_file, data)
    return data


def download_album_photos(album_id, output=None, async_mode=True):
    data = get_album_photos(album_id)
    album = data['album']
    photos = data['photos']
    output = os.path.abspath(output or _get_album_output(album))
    if not os.path.exists(output):
        os.makedirs(output)
    urls = [p.get('large') or p.get('image') for p in photos]
    if async_mode:
        return [executor.submit(download_file, url, output=output) for url in urls]
    else:
        return [download_file(url, output=output) for url in urls]


def get_albums_in_doulist(doulist_id):
    doulist_id = _compat_doulist_id(doulist_id)
    logger.info('get_albums_in_doulist %s' % doulist_id)
    output = _get_doulist_output()
    data_file = os.path.join(output, 'doulist_%s.dat' % doulist_id)
    if os.path.exists(data_file):
        albums = read_dict(data_file)
        logger.info('get_albums_in_doulist read %s' % doulist_id)
    else:
        albums = doubanweb.get_albums_in_doulist(doulist_id)
        logger.info('get_albums_in_doulist fetch %s' % doulist_id)
        if albums:
            write_dict(data_file, albums)
    return albums


def get_albums_in_all_doulist(doulist_ids):
    for did in doulist_ids:
        get_albums_in_doulist(did)


def combine_doulist_albums():
    data_file = os.path.join(OUTPUT_ROOT, 'doulist_albums.json')
    id_file = os.path.join(OUTPUT_ROOT, 'doulist_album_ids.json')
    all_albums = []
    all_ids = []
    output = _get_doulist_output()
    for name in os.listdir(output):
        if not name.endswith('.dat'):
            continue
        filename = os.path.join(output, name)
        albums = read_dict(filename)
        if albums:
            print('Combine %s (%s)' % (filename, len(albums)))
            all_albums.extend(albums)
            all_ids.extend([doubanweb.get_id_from_album_url(a[0]) for a in albums])
    all_albums = sorted(all_albums, key=lambda x: x[0])
    all_ids = distinct_list(all_ids, sort=True)
    write_dict(data_file, all_albums)
    write_file(id_file, ','.join(all_ids))
    print('Combined file: %s (%s)' % (data_file, len(all_albums)))


if __name__ == '__main__':
    # from albums_data import NEW_IDS as ids
    # get_albums_in_all_doulist(ids)
    combine_doulist_albums()
