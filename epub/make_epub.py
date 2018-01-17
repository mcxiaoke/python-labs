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

CHAPTER_TEMPLATE = 'chapter.xhtml'


def create_chapter(text_file, dst=None):
    if not isinstance(text_file, unicode):
        text_file = text_file.decode('utf-8')
    output = dst or os.path.dirname(text_file)
    # print('create_chapter from %s' % text_file)
    if not os.path.exists(output):
        os.makedirs(output)
    filename = os.path.basename(text_file)
    name, ext = os.path.splitext(filename)
    text_lines = read_list(text_file)
    text_lines = ['<p>%s</p>' % line for line in text_lines]
    text_str = '\n'.join(text_lines)
    html_tpl = read_file(CHAPTER_TEMPLATE)
    html_str = html_tpl.format(name, text_str)
    html_file = os.path.join(output, '%s.html' % name)
    write_file(html_file, html_str)
    print('create_chapter to %s' % html_file)
    return pypub.create_chapter_from_file(html_file, title=name)


def create_epub(src, dst):
    epub = pypub.Epub(u'中文标题测试', creator=u'mcxiaoke',
                      language=u'cn', rights=u'Nothing', publisher=u'Cat Public')
    count = 0
    for name in os.listdir(src):
        f = os.path.join(src, name)
        chapter = create_chapter(f, dst)
        epub.add_chapter(chapter)
        count += 1
        if count > 10:
            break
    epub.create_epub('.', epub_name='test-epub')


def main():
    src = sys.argv[1]
    dst = 'temp'
    create_epub(src, dst)


if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import commons
    from lib.utils import read_file, write_file, read_list, write_list
    main()
