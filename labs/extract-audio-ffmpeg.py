# -*- coding: utf-8 -*-
# @Author: Miu
# @Date:   2017-06-27 21:41:37
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2017-06-27 22:24:32
from __future__ import print_function
import sys
import os
import codecs
import re
import string
import shutil
import shlex
import subprocess
from os import path

VIDEO_FORMATS = ('.mp4', '.mkv', '.avi', '.wmv', '.flv', '.f4v', '.mpg', '.ts')


def get_audio_codec(fi):
    args = "ffprobe -v error -select_streams a:0 " \
        "-show_entries stream=codec_name -of " \
        "default=noprint_wrappers=1:nokey=1 {}".format(fi).split()
    return subprocess.check_output(args)


def process(curdir, name):
    # subprocess.check_call(["ls", "-l"])
    # subprocess.check_output(["echo", "Hello World!"])
    base, ext = path.splitext(name)
    fi = path.join(curdir, name)
    fo = os.path.join(curdir, '{}.wma'.format(base))
    print('input: {}'.format(fi))
    if ext.lower() not in VIDEO_FORMATS:
        return
    if os.path.exists(fo) and os.path.getsize(fo) > 0:
        return
    acodec = get_audio_codec(fi)
    # print('input audio codec: {}'.format(acodec))
    print('output: {}'.format(fo))
    # args = "ffmpeg -i {} -vn -c:a copy {}".format(fi, fo).split()
    # -c:a libfdk_aac -b:a 128k
    if acodec and acodec.strip() == 'aac':
        print('just copy original audio stream')
        args = "ffmpeg -hide_banner -v error -i {} -vn -c:a copy {}".format(
            fi, fo).split()
    else:
        print('need convert original audio stream')
        args = "ffmpeg -hide_banner -v error -i {} -vn -c:a libfdk_aac -vbr 4 {}".format(
            fi, fo).split()
    subprocess.call(args, stderr=subprocess.STDOUT)


def main(root):
    for curdir, subdirs, filenames in os.walk(root, topdown=True):
        print(u'-- {} --'.format(curdir))
        for name in filenames:
            process(curdir, name)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 2:
        print('Usage: {} target_dir'.format(sys.argv[0]))
        sys.exit(1)
    root = os.path.abspath(sys.argv[1])
    print('Root: {}'.format(root))
    main(root)
