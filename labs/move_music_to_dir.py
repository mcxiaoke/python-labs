# -*- coding: UTF-8 -*-
from __future__ import print_function
import os
import sys
import shutil

AUDIO_FORMATS = ('.m4a', '.aac', '.mp3', '.flac', '.ape')


def main(src, dst):
    for curdir, subdirs, filenames in os.walk(src, topdown=True):
        # print('-- {} --'.format(curdir))
        for name in filenames:
            base, ext = os.path.splitext(name)
            fi = os.path.join(curdir, name)
            fo = os.path.join(dst, name)
            if ext.lower() in AUDIO_FORMATS:
                if not os.path.exists(fo):
                    print('move {}'.format(fi))
                    shutil.move(fi, fo)
                else:
                    print('skip {}'.format(fi))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
