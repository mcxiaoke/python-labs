#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-17 13:59:14
# modified at 2024.02.01
from __future__ import unicode_literals, division, absolute_import, print_function
import codecs
import base64
import json
import sys
import re
import os
import time
import shutil
import random
import argparse
import traceback
import textwrap
import chardet
import pypinyin
import pypub
from itertools import zip_longest
from multiprocessing import Process
from lib import compat
from lib import commons
from lib import unipath as upath
from lib import text
from lib.utils import read_file, write_file, read_list, now, files_size, humanize_bytes

__version__ = "0.2.0"

MAX_CH_COUNT = 3000
SIZE_M = 1024 * 1024
DEFAULT_BOOK_SIZE = 60  # in MB
MAX_BOOK_SIZE = 300  # in MB
CHAPTER_TEMPLATE = "resources/chapter.xhtml"
BASE = os.path.dirname(__file__)


def create_html_from_text(text_file, dst=None):
    output = dst or os.path.dirname(text_file)
    # print('create_chapter from %s' % text_file)
    if not os.path.exists(output):
        os.makedirs(output)
    filename = os.path.basename(text_file)
    name, ext = os.path.splitext(filename)
    html_file = os.path.join(output, "%s.html" % name)
    if os.path.exists(html_file):
        return html_file, name
    else:
        text_lines = read_list(text_file)
        text_lines = ["<p>%s</p>" % line for line in text_lines]
        # first line as title, h2
        body_str = "\n".join(text_lines)
        html_tpl = read_file(CHAPTER_TEMPLATE)
        html_str = html_tpl.format(name, name, body_str)
        write_file(html_file, html_str)
        print("create_chapter to %s" % html_file)
        return html_file, name


def _create_epub_single(files, output, title):
    import pypub

    chapters = []
    # https://docs.python.org/3/library/codecs.html
    ch_index = 0
    for file in files:
        ch_index += 1
        if not file or not os.path.exists(file):
            continue
        name = os.path.basename(file)
        if name and name.startswith("ch_"):
            print("[%s] Skip %s [%02d]" % (title, file, ch_index))
            continue
        # print("Parsing file %s" % file)
        c_file = file
        c_title = text.normalize_filename(os.path.splitext(name)[0])[:16]
        c_content = text.read_content(c_file)
        if c_content and len(c_content) > 8192:
            print("[%s] Adding %s <%s> [%02d]" % (title, c_title, name, ch_index))
            chapters.append((c_content, c_title))

    sort_by_pinyin = lambda x: [
        pypinyin.pinyin(i, style=pypinyin.Style.TONE3) for i in x[1]
    ]
    chapters = sorted(chapters, key=sort_by_pinyin)
    creator = "Epub2024"
    language = "cn"
    rights = now()
    publisher = "Epub2024"
    print('Creating epub "%s" include %s chapters' % (title, len(chapters)))
    cover_file = os.path.join(BASE, "resources", "cover.jpg")
    book = pypub.Epub(
        title,
        cover=cover_file,
        creator=creator,
        language=language,
        rights=rights,
        publisher=publisher,
    )
    for ch in chapters:
        # print("Adding chapter %s" % ch[1])
        book.add_chapter(pypub.create_chapter_from_text(*ch))
    book_file = os.path.join(output, "%s.epub" % title)
    if os.path.exists(book_file):
        os.remove(book_file)
    book.create(book_file)
    print("Created epub file: %s" % book_file)


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
    print("Chunks count=%s size=%s" % (len(chunks), humanize_bytes(total)))
    return chunks


def grouper(iterable, n, padvalue=None):
    return list(zip_longest(*[iter(iterable)] * n, fillvalue=padvalue))


def create_epub_multi(all_files, output, title_prefix, max_count=0, max_size=0):
    total_count = len(all_files)
    chunk_by_count = max_count > 0
    if chunk_by_count:
        chunk_count = max_count or MAX_CH_COUNT
        files_chunks = grouper(all_files, min(chunk_count, MAX_CH_COUNT))
    else:
        chunk_size = max_size * SIZE_M or DEFAULT_BOOK_SIZE
        files_chunks = slice_by_size(all_files, min(chunk_size, DEFAULT_BOOK_SIZE))
    page_no = 1
    ps = []
    for i in range(0, len(files_chunks)):
        files = files_chunks[i]
        n = len(files)
        # title = "%s Vol %s (%s-%s)" % (title_prefix,
        #                                i + 1, page_no, page_no + n)
        title = "%s-%02d" % (title_prefix, i + 1)
        page_no += n
        ps.append(create_epub_single(files, output, title=title))
    for p in filter(None, ps):
        p.join()


def create_epub(src, output, title, max_count=0, max_size=0):
    if not os.path.isdir(src):
        raise IOError('src "%s" not exists' % src)
    if not title:
        raise ValueError("title must not be empty")
    if max_size > MAX_BOOK_SIZE:
        raise ValueError("max_size must between (%s - %s) (in MB)" % (1, MAX_BOOK_SIZE))
    src = upath.pathof(src)
    output = upath.abspath(output or os.path.dirname(src))
    title = compat.to_text(title)
    print(
        "Create epub from [%s] to [%s], title is [%s], max size is [%sMB]"
        % (src, output, title, max_size)
    )

    def is_html_or_text(n):
        return n.lower().endswith(".txt") or n.lower().endswith(".html")

    files = [os.path.join(src, n) for n in os.listdir(src) if is_html_or_text(n)]
    multi_mode = max_count > 0 or max_size > 0
    if multi_mode:
        create_epub_multi(files, output, title, max_count, max_size)
    else:
        p = create_epub_single(files, output, title)
        if p:
            p.join()


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Easy ePub Maker v{0}".format(__version__),
        epilog="""https://github.com/mcxiaoke/python-labs
        """,
    )
    parser.add_argument("input", help="Source text or html files")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("-t", "--title", help="ePub book title")
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=0,
        help="Max chapter count per book",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        default=0,
        help="Max size per book (in MB)",
    )
    # parser.add_argument('-m', '--mode', choices=('count', 'size'), default='size')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def main():
    args = vars(parse_args())
    print(args)
    src = upath.abspath(args.get("input"))
    dst = args.get("output")
    title = args.get("title")
    max_count = args.get("count") or 0
    max_size = args.get("size") or 0

    sub_dirs = sorted(os.listdir(src))
    sub_dirs = [os.path.join(src, x) for x in sub_dirs]
    use_batch_mode = len(sub_dirs) < 20 and all(os.path.isdir(x) for x in sub_dirs)
    if use_batch_mode:
        for sub_dir in sub_dirs:
            print("Processing {}".format(sub_dir))
            sub_title = os.path.basename(sub_dir)
            sub_title = "{}_Book".format(
                pypinyin.pinyin(sub_title, style=pypinyin.Style.FIRST_LETTER)
            ).upper()
            create_epub(sub_dir, dst, sub_title, max_count, max_size)
    else:
        create_epub(src, dst, title, max_count, max_size)


def profile():
    import cProfile

    cProfile.run("demo()")


if __name__ == "__main__":
    sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    main()
    a = ""
    # profile()
