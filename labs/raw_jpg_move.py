#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
from os import path
import sys
import shutil
import re


def move_all_jpeg(src_dir):
    src_dir = os.path.abspath(src_dir)
    print('Root:{}'.format(src_dir))
    index = 0
    tasks = []
    for root, dirs, files in os.walk(src_dir):
        for d in dirs:
            if d == 'JPEG':
                # From RAW2/20201125：XXXXXX/landscape/JPEG
                # Toto JPEG/20201125：XXXXXX/landscape
                jpg_raw_dir = os.path.join(root, d)
                jpg_dir_name = os.path.basename(root)
                jpg_dir_root_new = root.replace('RAW', 'JPEG')
                tasks.append((jpg_raw_dir, jpg_dir_root_new))
                print('Prepare:{}'.format(jpg_raw_dir))
                ###
                # jpg_dir_root_new = jpg_dir_root_new.replace(jpg_dir_name, '')
                # print('Rename: {}'.format(jpg_raw_dir_new))
                # os.rename(jpg_raw_dir, jpg_raw_dir_new)
                # if not os.path.exists(jpg_dir_root_new):
                #     os.makedirs(jpg_dir_root_new)
                #     print('Make Dir: {}'.format(jpg_dir_root_new))
                ###

    print('\n{} JPEG folders to be moved, Are you sure? yes/no'.format(len(tasks)))
    answer = input()
    if answer.startswith('y'):
        for f, t in tasks:
            print('FR {}'.format(f))
            # shutil.move(f, t)
            # custom move function
            tp = os.path.dirname(t)
            if not os.path.exists(tp):
                os.makedirs(tp)
            os.rename(f, t)
            print('TO {}'.format(t))
        print('All done.')
    else:
        print('Ignored Tasks: ')
        for f, t in tasks:
            print('FR {}'.format(f))
            print('TO {}'.format(t))
        print('Aborted, nothing to do.')


if __name__ == '__main__':
    move_all_jpeg(sys.argv[1])
