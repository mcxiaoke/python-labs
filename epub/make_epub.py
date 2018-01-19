#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-17 13:59:14
from __future__ import print_function
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


def create_epub(src, dst):
    import pypub
    book = pypub.Epub(u'ePub Book', creator=u'test',
                      language=u'cn', rights=u'test', 
                      publisher=u'test',)
    count = 0
    html_files = []
    for name in os.listdir(src):
        f = os.path.join(src, name)
        html_files.append(create_html_from_text(f, dst))
        count += 1
        if count > 3:
            break
    
    for file,title in html_files:
        book.add_chapter(pypub.create_chapter_from_file(file, title))
    # book.add_chapter(pypub.create_chapter_from_url('https://www.zhihu.com/question/19991740/answer/141072770'))
    # book.add_chapter(pypub.create_chapter_from_url('https://baike.baidu.com/item/%E7%8C%AB%E5%92%AA'))
    # book.add_chapter(pypub.create_chapter_from_url('https://www.douban.com/review/9080557/'))
    # book.add_chapter(pypub.create_chapter_from_url('http://www.cnblogs.com/vamei/archive/2012/09/13/2682778.html'))
    book.add_chapter(pypub.create_chapter_from_url('https://www.douban.com/note/654068918/'))
    book.create_epub(os.path.dirname(dst),
                     epub_name='test')


def main():
    src = sys.argv[1]
    dst = os.path.expanduser('~/Downloads/epub_temp')
    create_epub(src, dst)
    # os.popen('open %s' % os.path.dirname(dst))


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import commons
    from lib.utils import read_file, write_file, read_list, write_list
    main()
