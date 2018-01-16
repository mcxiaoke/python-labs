# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-03-07 14:37:26
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2018-01-11 21:37:06
from __future__ import print_function
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
from doubanutils import api,upload_photos_to_album

TEST_ALBUM_ID = '1657031875'

def upload_photos():
    print(sys.argv)
    if len(sys.argv) < 3:
        print('Usage: %s album_id photos_dir' % sys.argv[0])
        exit(1)
    album_id = sys.argv[1]
    photos = os.path.abspath(sys.argv[2])
    upload_photos_to_album(album_id, photos)

def main():
    api.debug = True
    api.me()
    upload_photos()


if __name__ == '__main__':
    main()