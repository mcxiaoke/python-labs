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

__version__ = '0.1.0'

DEFAULT_CHAPTERS_COUNT = 500
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

def create_epub_single(files, output, title):
    import pypub
    creator = "Anonymous"
    language = 'cn'
    rights = now()
    publisher = 'Anonymous'
    print('Creating epub: <%s>' % title)
    book = pypub.Epub(title, creator=creator,
                    language=language, rights=rights, 
                    publisher=publisher)
    for file in files:
        name = os.path.basename(file)
        c_title = os.path.splitext(name)[0]
        c_file = file
        book.add_chapter(pypub.create_chapter_from_file(c_file, c_title))
    book.create_epub(output, epub_name=title)

def create_epub_volumes(all_files, output, title_prefix, max_count=DEFAULT_CHAPTERS_COUNT):
    files_chunks = slice_list(all_files, max_count)
    page_no = 1
    for i in range(0, len(files_chunks)):
        files = files_chunks[i]
        n = len(files)
        title = "%s Vol %s (%s-%s)" % (title_prefix, i+1, page_no, page_no+n)
        page_no += n
        create_epub_single(files, output, title=title)

def create_epub(src, output, title, max_count=DEFAULT_CHAPTERS_COUNT):
    src = upath.pathof(src)
    title = enc.unicode_string(title or 'ePub Book')
    def is_html_or_text(n):
        return n.lower().endswith('.txt') or n.lower().endswith('.html')
    files = [os.path.join(src, n) for n in os.listdir(src) if is_html_or_text(n)]
    if len(files) > max_count:
        create_epub_volumes(files, output, title, max_count)
    else:
        create_epub_volume(files, output, title, max_count)

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Easy ePub Maker v{0}'.format(__version__),
        epilog='''https://github.com/mcxiaoke/python-labs
        ''')
    parser.add_argument('input', help='Source text or html files')
    parser.add_argument('-o', '--output',
                        help='Output directory')
    parser.add_argument('-t', '--title', default='ePub Book',
                        help='ePub book title')
    parser.add_argument('-c', '--count', type=int, default=DEFAULT_CHAPTERS_COUNT,
                        help='Max chapters per book')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()

def main():
    args = vars(parse_args())
    print(args)
    src = upath.pathof(args.get('input'))
    if args.get('output'):
        dst = upath.pathof(args.get('output'))
    else:
        dst = os.path.abspath('temp')
    title = args.get('title')
    max_count = args.get('count')
    create_epub(src, dst, title, max_count)
    

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import commons
    from lib import upath
    from lib import enc
    from lib.utils import read_file, write_file, read_list, write_list, slice_list, now
    main()
