# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-03-07 14:37:26
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2018-01-11 21:37:06
from __future__ import print_function, unicode_literals, absolute_import
import sys
import os
import argparse
import traceback
from doubanutils import api,upload_photos_to_album

__version__ = '0.1.0'

TEST_ALBUM_ID = '1657031875'

def upload_photos(album_id, photos):
    api.debug = True
    api.me()
    upload_photos_to_album(album_id, photos)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Douban Photos Uploader v%s' % __version__,
        epilog='https://github.com/mcxiaoke/python-labs')
    parser.add_argument('album_id', help='target album id for uploading photos')
    parser.add_argument('photos', help='photos directory')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

def main():
    args = vars(parse_args())
    print(args)
    album_id = args.get('album_id')
    photos = os.path.abspath(args.get('photos'))
    upload_photos(album_id, photos)

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    main()