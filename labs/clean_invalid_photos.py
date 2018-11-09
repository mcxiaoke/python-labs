# -*- coding: UTF-8 -*-

from __future__ import print_function
import os, sys
from os import path


def handler(arg, dirname, names):
    dir_path = path.join(dirname, dirname)
    for name in names:
        file_path = path.abspath(path.join(dirname, name))
        if name.startswith("._"):
            os.remove(file_path)
            print("delete file: %s." % file_path)


os.path.walk(path.normcase(sys.argv[1]), handler, ())
