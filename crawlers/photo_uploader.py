# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-03-07 14:37:26
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2016-03-07 17:25:13
from __future__ import print_function
import codecs
import requests
import base64
import json
import sys
import os
import time
import shutil
from doubanapi import ApiClient
from utils import read_list, write_list

from config import API_KEY, API_SECRET, USERNAME, PASSWORD

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 3:
        print('Usage: python %s album_id dir' % sys.argv[0])
        exit(1)
    api = ApiClient(key=API_KEY, secret=API_SECRET)
    print(api.login(USERNAME, PASSWORD))
    album = sys.argv[1]
    directory = sys.argv[2]
    files = os.listdir(directory)
    finished = read_list('%s.txt' % album)
    error_count = 0
    for f in files:
        image = os.path.join(directory, f)
        try:
            if f not in finished:
                print('Uploading %s' % image)
                api.photo_upload(album, image, f)
                finished.append(image)
                time.sleep(2)
        except Exception, e:
            print("error:%s on uploading :%s" % (e, image))
            error_count += 1
            if error_count > 5:
                break
            time.sleep(error_count * 10)
    write_list('%s.txt' % album, finished)
