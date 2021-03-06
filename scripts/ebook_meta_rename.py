'''
File: ebook_fix.py
Created: 2021-03-06 15:46:09
Modified: 2021-03-06 15:46:14
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''
import sys
import os
from pprint import pprint
from types import new_class
from mobi import Mobi
from ebooklib import epub
import argparse
from multiprocessing.dummy import Pool
from functools import partial

RET_OK = 0
RET_IGNORE = -1
RET_SKIP = -2
RET_PARSE_ERROR = -101
RET_OS_ERROR = -102

BOOK_FORMATS = ('.mobi', '.azw', '.azw3', '.epub')


class BookParser:

    def __init__(self, src):
        self.src = src
        self.src_dir = os.path.dirname(src)
        self.src_name = os.path.basename(src)
        self.dst = None
        self.dst_name = None
        self.parse()

    def parse(self):
        raise('subclass must override this')

    def check(self):
        if not self.dst_name or not self.dst:
            return RET_PARSE_ERROR
        elif self.dst_name == self.src_name:
            return RET_IGNORE
        elif os.path.exists(self.dst):
            return RET_SKIP
        else:
            print('Name Before:\t{}'.format(self.src_name))
            print('Name After:\t{}'.format(self.dst_name))

    def rename(self):
        if not self.dst_name or not self.dst:
            # print('Bad Format:\t{}'.format(self.dst_name))
            return RET_PARSE_ERROR
        elif self.dst_name == self.src_name:
            # print('Good Book:\t{}'.format(self.dst_name))
            return RET_IGNORE
        elif os.path.exists(self.dst):
            # print('Skip Book:\t{}'.format(self.dst_name))
            return RET_SKIP
        else:
            try:
                # print('Rename From:\t{}'.format(self.src_name))
                print('Rename To:\t{}'.format(self.dst_name))
                os.rename(self.src, self.dst)
                return RET_OK
            except Exception as e:
                print("Rename Error:\t{}".format(e))
                return RET_OS_ERROR


class MobiParser(BookParser):
    # using lib mobi-python
    def __init__(self, src):
        super().__init__(src)

    def parse(self):
        base, ext = os.path.splitext(self.src_name)
        ext = ext and ext.lower()
        try:
            book = Mobi(self.src)
            book.parse()
            title = book.config['mobi']['Full Name'].decode('utf8')
            self.dst_name = '{}{}'.format(title, ext)
            self.dst = os.path.join(self.src_dir, self.dst_name)
            # print('Mobi Title:\t{}'.format(self.dst_name))
        except Exception as e:
            print("Parse Error:\t{}".format(e))


class EpubParser(BookParser):
    # using lib
    def __init__(self, src):
        super().__init__(src)

    def parse(self):
        base, ext = os.path.splitext(self.src_name)
        ext = ext and ext.lower()
        try:
            book = epub.read_epub(self.src)
            title = book.title
            self.dst_name = '{}{}'.format(title, ext)
            self.dst = os.path.join(self.src_dir, self.dst_name)
            # print('EPub Title:\t{}'.format(self.dst_name))
        except Exception as e:
            print("Parse Error:", e)


def list_files(source, recrusily=False, ext_filter=None):
    files = []
    if not recrusily:
        names = os.listdir(source)
        if not ext_filter:
            files.extend([os.path.join(source, name) for name in names])
        else:
            for name in names:
                _, ext = os.path.splitext(name)
                if ext and ext.lower() in ext_filter:
                    files.append(os.path.join(source, name))
    else:
        for root, dirs, names in os.walk(source):
            if not ext_filter:
                files.extend([os.path.join(root, name) for name in names])
            else:
                for name in names:
                    _, ext = os.path.splitext(name)
                    if ext and ext.lower() in ext_filter:
                        files.append(os.path.join(root, name))
    return files


def rename_one_book(fname, idx, total, execute=False):
    print('Task({}/{}):\t{}'.format(idx, total, fname))
    name = os.path.basename(fname)
    _, ext = os.path.splitext(name)
    if ext in ('.mobi', '.azw', '.azw3'):
        book = MobiParser(fname)
    elif ext == '.epub':
        book = EpubParser(fname)
    else:
        print('Unknown Format: {}'.format(name))
        book = None
    if book:
        if execute:
            book.rename()
        else:
            book.check()


def rename_books(source, execute=False, recrusily=False):
    print('=== Source: {} ==='.format(source))
    files = list_files(source, recrusily, BOOK_FORMATS)
    total = len(files)
    p = Pool(8)
    try:
        for idx, fname in enumerate(files):
            # print('Processing({}/{}):\t{}'.format(idx, total, fname))
            # partial_rename_one = partial(rename_one_book, execute=execute)
            # rename_one_book(fname, execute)
            p.apply_async(rename_one_book, (fname, idx, total, execute))
        p.close()
        p.join()
    except KeyboardInterrupt:
        print('Warning: User Ctrl-C inerrupt, abort.')
        p.terminate()
        # sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source', help='Source folder contains ebooks')
    parser.add_argument('-e', '--execute', action='store_true',
                        help='Rename all ebooks [default:False]')
    parser.add_argument('-r', '--recrusily', action='store_true',
                        help='Process books in source folder recursively [default:False]')
    args = parser.parse_args()
    print(args)
    rename_books(args.source, args.execute, args.recrusily)
