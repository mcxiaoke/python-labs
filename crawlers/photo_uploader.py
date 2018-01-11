# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-03-07 14:37:26
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2018-01-11 15:13:06
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
import traceback
from doubanapi import ApiClient
from utils import read_list, write_list

from config import USERNAME, PASSWORD

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 3:
        print('Usage: python %s album_id dir' % sys.argv[0])
        exit(1)
    api = ApiClient()
    api.login(USERNAME, PASSWORD)
    album = sys.argv[1]
    directory = sys.argv[2]
    files = os.listdir(directory)
    done_file = os.path.join(directory, '%s_done.txt' % album)
    finished = read_list(done_file)
    error_count = 0
    for f in files:
        image = os.path.join(directory, f)
        try:
            if f not in finished:
                print('Uploading %s' % image)
                api.photo_upload(album, image, f)
                finished.append(f)
                write_list(done_file, finished)
                time.sleep(random.randint(1, 3))
            else:
                print('Skip %s' % image)
        except Exception, e:
            print("Error:%s On uploading :%s" % (e, image))
            traceback.print_exc()
            error_count += 1
            if error_count > 5:
                break
            time.sleep(error_count * 10)
    write_list(done_file, finished)
