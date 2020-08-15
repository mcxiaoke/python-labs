#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2020-08-09
import os
import time
from os import path
import sys
import shutil
import re


def copy_pics(src_dir):
    index = 0
    images = []
    for root, dirs, files in os.walk(src_dir):
        for adir in dirs:
            if 'thumb' in adir.lower():
                continue
        for name in files:
            src_path = path.abspath(path.join(root, name))
            index = index + 1
            images.append((src_path, dst_path, index))
            print("Prepare: {}".format(src_path))
    total = len(images)
    print('{} images will be processed.'.format(total))
    sel = input("Press Enter yes or y to continue...")
    if not sel.startswith("y"):
        print("Aborted.")
        return
    start = time.time()
    # todo
    elapsed = time.time()-start
    print("Task finished, {} files, using {} seconds.".format(total, elapsed))


if __name__ == '__main__':
    copy_pics(sys.argv[1])
