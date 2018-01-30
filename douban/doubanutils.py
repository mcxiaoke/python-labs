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
from operator import itemgetter
from lxml import etree, html
from doubanapi import ApiClient, COUNT
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

OUTPUT_ROOT = 'output'
DOUBAN_ROOT = os.path.join(OUTPUT_ROOT, 'douban')
if not os.path.exists(DOUBAN_ROOT):
    os.makedirs(DOUBAN_ROOT)

executor = ThreadPoolExecutorStackTraced(max_workers=8)

token_file = os.path.join(get_user_home(), '.douban_token.dat')
api = ApiClient(token_file=token_file)


def _get_downloads_output(root=DOUBAN_ROOT):
    return os.path.join(root, 'downloads')


def _get_album_photos_output(album, root=DOUBAN_ROOT):
    album_name = get_valid_filename(album['title'])
    return os.path.join(_get_downloads_output(root), '%s_%s' % (album_name, album['id']))


def _get_albums_output(root=DOUBAN_ROOT):
    return os.path.join(root, 'albums')


def _get_doulist_output(root=DOUBAN_ROOT):
    return os.path.join(root, 'doulist')


def _get_user_output(root=DOUBAN_ROOT):
    return os.path.join(root, 'user')


def _compat_album_id(param):
    # compat for param is album url
    if '/photos/album/' in param:
        return doubanweb.get_id_from_album_url(param)
    else:
        return param


def _compat_doulist_id(param):
    # compat for param is doulist url
    if '/doulist/' in param:
        return doubanweb.get_id_from_doulist_url(param)
    else:
        return param


def _compat_user_id(param):
    # compat for param is people url
    if '/people/' in param:
        return doubanweb.get_id_from_user_url(param)
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
    while True:
        data = api.album_photos(album_id, start=len(photos), count=COUNT)
        new_photos = data['photos']
        if not new_photos:
            break
        logger.info('fetch_album_photos %s new photos found in %s'
                    % (len(new_photos), album_id))
        # new_urls = [p.get('large') or p.get('image') for p in photos]
        photos.extend(new_photos)
        time.sleep(random.randint(0, 5))
        if len(new_photos) < COUNT / 2:
            break
        if len(photos) > 600:
            # max photos = 600
            break
    logger.info('fetch_album_photos %s photos found in %s'
                % (len(photos), album_id))
    if photos:
        data['photos'] = photos
        return data


def get_album_photos(album_id, root=DOUBAN_ROOT):
    # https://api.douban.com/v2/album/1622166069/photos
    album_id = _compat_album_id(album_id)
    logger.info('get_album_photos %s' % album_id)
    output = _get_albums_output(root)
    if not os.path.exists(output):
        os.makedirs(output)
    data_file = os.path.join(output, 'album_%s.dat' % album_id)
    if os.path.exists(data_file):
        data = read_dict(data_file)
        logger.info('get_album_photos read %s' % album_id)
    else:
        data = _fetch_album_photos(album_id)
        logger.info('get_album_photos fetch %s' % album_id)
        if data:
            write_dict(data_file, data)
    return data


def download_album_photos(album_id, root=DOUBAN_ROOT, async_mode=True):
    logger.info('download_album_photos %s' % album_id)
    data = get_album_photos(album_id, root)
    album = data['album']
    photos = data['photos']
    output =  _get_album_photos_output(album, root)
    if not os.path.exists(output):
        os.makedirs(output)
    urls = [p.get('large') or p.get('image') for p in photos]
    if async_mode:
        return [executor.submit(download_file, url, output=output) for url in urls]
    else:
        return [download_file(url, output=output) for url in urls]


def _fetch_albums_for_user(user_id):
    user_id = _compat_user_id(user_id)
    logger.info('_fetch_albums_for_user user %s' % user_id)
    data = None
    albums = []
    while True:
        data = api.user_albums(user_id, start=len(albums), count=COUNT)
        new_albums = data['albums']
        if not new_albums:
            break
        logger.info('_fetch_albums_for_user %s new albums found for %s'
                    % (len(new_albums), user_id))
        albums.extend(new_albums)
        if len(new_albums) < COUNT / 2:
            break
    logger.info('_fetch_albums_for_user %s albums found for %s'
                % (len(albums), user_id))
    keep_keys = ('title', 'alt', 'id')
    return [{k: a[k] for k in keep_keys} for a in albums]


def get_albums_for_user(user_id, root=DOUBAN_ROOT):
    user_id = _compat_user_id(user_id)
    logger.info('get_albums_for_user %s' % user_id)
    output = _get_user_output(root)
    if not os.path.exists(output):
        os.makedirs(output)
    data_file = os.path.join(output, 'user_%s.json' % user_id)
    if os.path.exists(data_file):
        albums = read_dict(data_file)
        logger.info('get_albums_for_user read %s' % user_id)
    else:
        albums = _fetch_albums_for_user(user_id)
        logger.info('get_albums_for_user fetch %s' % user_id)
        if albums:
            write_dict(data_file, albums)
    return albums


def download_user_photos(user_id, root=DOUBAN_ROOT, async_mode=True):
    albums = get_albums_for_user(user_id, root)
    album_ids = [album['id'] for album in albums]
    for album_id in album_ids:
        download_album_photos(album_id, root=root, async_mode=async_mode)


def get_albums_in_doulist(doulist_id, root=DOUBAN_ROOT):
    doulist_id = _compat_doulist_id(doulist_id)
    logger.info('get_albums_in_doulist %s' % doulist_id)
    output =  _get_doulist_output(root)
    if not os.path.exists(output):
        os.makedirs(output)
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


def download_doulist_photos(doulist_id, root=DOUBAN_ROOT, async_mode=True):
    albums = get_albums_in_doulist(doulist_id, root)
    album_ids = [doubanweb.get_id_from_album_url(a[0]) for a in albums]
    for album_id in album_ids:
        download_album_photos(album_id, root=root, async_mode=async_mode)


def get_albums_in_all_doulist(doulist_ids):
    for did in doulist_ids:
        get_albums_in_doulist(did)


def combine_doulist_albums():
    data_file = os.path.join(DOUBAN_ROOT, 'albums.json')
    id_file = os.path.join(DOUBAN_ROOT, 'album_ids.json')
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
            all_ids.extend([doubanweb.get_id_from_album_url(a[0])
                            for a in albums])
    all_albums = sorted(all_albums, key=itemgetter(0))
    all_ids = distinct_list(all_ids, sort=True)
    write_dict(data_file, all_albums)
    write_file(id_file, ','.join(all_ids))
    print('Combined file: %s (%s)' % (data_file, len(all_albums)))


def download_all_album_photos(root=DOUBAN_ROOT):
    id_file = os.path.join(root, 'album_ids.json')
    ids = read_file(id_file).split(',')
    print(len(ids))
    blacklist = ['100945526', '100075813']
    for id in ids:
        if id not in blacklist:
            executor.submit(download_album_photos, id, async_mode=False)
            # download_album_photos(id)

def download_cat_photos():
    root = os.path.join(OUTPUT_ROOT, 'cats')
    doulist_ids = ['3982978', '4189996']
    for did in doulist_ids:
        albums = get_albums_in_doulist(did, root)
        album_ids = [doubanweb.get_id_from_album_url(a[0]) for a in albums]
        for album_id in album_ids:
            executor.submit(download_album_photos, album_id, root=root, async_mode=False)

if __name__ == '__main__':
    print('doubanutils')
    # from albums_data import NEW_IDS as ids
    # get_albums_in_all_doulist(ids)
    # combine_doulist_albums()
    # download_all_album_photos()
    # get_all_album_photos()
    # download_user_photos('1233832')
    # download_doulist_photos('1867090')
    download_cat_photos()
