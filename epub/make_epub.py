#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-17 13:59:14
from __future__ import unicode_literals, division, absolute_import, print_function
import codecs
import base64
import json
import sys
import os
import time
import shutil
import random
import argparse
import traceback
import textwrap
import pypub
from multiprocessing import Process

__version__ = '0.1.0'

MAX_CH_COUNT = 500
SIZE_M = 1024 * 1024
DEFAULT_BOOK_SIZE = 40  # in MB
MAX_BOOK_SIZE = 200  # in MB
CHAPTER_TEMPLATE = 'resources/chapter.xhtml'


def create_html_from_text(text_file, dst=None):
    if not isinstance(text_file, unicode):
        text_file = text_file.decode('utf-8')
    output = dst or os.path.dirname(text_file)
    # print('create_chapter from %s' % text_file)
    if not os.path.exists(output):
        os.makedirs(output)
    filename = os.path.basename(text_file)
    name, ext = os.path.splitext(filename)
    html_file = os.path.join(output, '%s.html' % name)
    if os.path.exists(html_file):
        return html_file, name
    else:
        text_lines = read_list(text_file)
        text_lines = ['<p>%s</p>' % line for line in text_lines]
        # first line as title, h2
        body_str = '\n'.join(text_lines)
        html_tpl = read_file(CHAPTER_TEMPLATE)
        html_str = html_tpl.format(name, name, body_str)
        write_file(html_file, html_str)
        print('create_chapter to %s' % html_file)
        return html_file, name

def _create_epub_single(files, output, title):
    import pypub
    creator = "Anonymous"
    language = 'cn'
    rights = now()
    publisher = 'Anonymous'
    print('Creating epub "%s" include %s chapters' % (title, len(files)))
    book = pypub.Epub(title, creator=creator,
                      language=language, rights=rights,
                      publisher=publisher)
    for file in files:
        name = os.path.basename(file)
        c_title = os.path.splitext(name)[0]
        c_file = file
        book.add_chapter(pypub.create_chapter_from_file(c_file, c_title))
    book.create_epub(output, epub_name=title)

def create_epub_single(files, output, title):
    p = Process(target=_create_epub_single, args=(files, output, title))
    p.start()
    return p
    # _create_epub_single(files, output, title)

def slice_by_size(all_files, max_size):
    max_size = max_size * SIZE_M
    chunks = []
    size = 0
    chunk = []
    total = 0
    index = 0
    for f in all_files:
        chunk.append(f)
        size += os.path.getsize(f)
        index += 1
        if size > max_size or index == len(all_files):
            chunks.append(chunk)
            total += size
            # print('Chunk %s items=%s size=%s' %(len(chunks), len(chunk), humanize_bytes(size)))
            size = 0
            chunk = []
    print('Chunks count=%s size=%s' % (len(chunks), humanize_bytes(total)))
    return chunks


def create_volumes_by_size(all_files, output, title_prefix, max_size=DEFAULT_BOOK_SIZE):
    # files_chunks = slice_list(all_files, max_count)
    files_chunks = slice_by_size(all_files, max_size)
    page_no = 1
    ps = []
    for i in range(0, len(files_chunks)):
        files = files_chunks[i]
        n = len(files)
        # title = "%s Vol %s (%s-%s)" % (title_prefix,
        #                                i + 1, page_no, page_no + n)
        title = "%s Vol %s" % (title_prefix, i + 1)
        page_no += n
        ps.append(create_epub_single(files, output, title=title))
    for p in filter(None,ps):
        p.join()


def create_epub(src, output, title, max_size=DEFAULT_BOOK_SIZE):
    if not os.path.isdir(src):
        raise IOError('src "%s" not exists' % src)
    if not title:
        raise ValueError('title must not be empty')
    if max_size > 100:
        raise ValueError('max_size must between (%s - %s) (in MB)' %
                         (1, MAX_BOOK_SIZE))
    src = upath.pathof(src)
    output = upath.abspath(output or 'temp')
    title = compat.to_text(title)
    print('Create epub from [%s] to [%s], title is [%s], max size is [%sMB]'
          % (src, output, title, max_size))

    def is_html_or_text(n):
        return n.lower().endswith('.txt') or n.lower().endswith('.html')
    files = [os.path.join(src, n)
             for n in os.listdir(src) if is_html_or_text(n)]
    if files_size(files) > max_size * SIZE_M:
        create_volumes_by_size(files, output, title, max_size)
    else:
        p = create_epub_single(files, output, title)
        if p:
            p.join()


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Easy ePub Maker v{0}'.format(__version__),
        epilog='''https://github.com/mcxiaoke/python-labs
        ''')
    parser.add_argument('input', help='Source text or html files')
    parser.add_argument('-o', '--output',
                        help='Output directory')
    parser.add_argument('-t', '--title', help='ePub book title')
    parser.add_argument('-s', '--size', type=int, default=DEFAULT_BOOK_SIZE,
                        help='Max size per book (in MB)')
    # parser.add_argument('-m', '--mode', choices=('count', 'size'), default='size')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def main():
    args = vars(parse_args())
    print(args)
    src = upath.abspath(args.get('input'))
    dst = args.get('output')
    title = args.get('title')
    max_size = args.get('size')
    create_epub(src, dst, title, max_size)

def profile():
    import cProfile
    cProfile.run('demo()')

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import compat
    from lib import commons
    from lib import upath
    from lib.utils import read_file, write_file, read_list, write_list, slice_list, now, files_size
    from lib.utils2 import humanize_bytes
    main()
    a = ''
    # profile()
