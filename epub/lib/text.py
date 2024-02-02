#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
import pathlib
import codecs
import chardet
import zhconv
import zhon
from chardet.universaldetector import UniversalDetector

UTF8_SUFFIX = "_utf8"

RE_PREFIX_SPE = re.compile(r"^(【|\[).+?(】|\])")
RE_PREFIX_ASCII = re.compile(r"^[!-~]+")
RE_NON_CHAR = re.compile(r"[^0-z{}]+".format(zhon.hanzi.characters))


def normalize_filename(s):
    # \u4e00-\u9fa5
    # https://www.jianshu.com/p/fcbc5cd06f39
    if re.compile(r"^【|\[\w+】|\]$").match(s):
        s = re.compile("[\[\]【】]").sub("", s)
    s = re.sub(RE_PREFIX_SPE, "", s)
    s = re.sub(RE_PREFIX_ASCII, "", s)
    s = re.sub(RE_NON_CHAR, "", s)
    s = zhconv.convert(s, "zh-cn")
    s = re.compile("^\u4e71\u4f26").sub("", s)
    s = re.compile("作者|完|全").sub("", s)
    return s.strip()


def normalize_content(s):
    s = re.compile(r"[^!-~{}]".format(zhon.hanzi.sentence)).sub("", s)
    s = re.compile("\w(\r\n)\w").sub("", s)
    s = re.compile(" {2,}").sub(" ", s)
    s = re.compile("[\r\n]{3,}").sub("\n\n", s)
    s = zhconv.convert(s, "zh-cn")
    return s


def detect_encoding(src):
    try:
        detector = UniversalDetector()
        with open(src, "rb") as f:
            for line in f:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        return detector.result
    except Exception as e:
        return None


def read_content(src, clean=False):
    content = None
    try:
        fenc = detect_encoding(src)
        enc = fenc and fenc["encoding"]
        if not enc:
            with codecs.open(src, mode="r", encoding="utf8") as f:
                content = f.read()
        else:
            if "gb" in enc.lower():
                with codecs.open(src, mode="r", encoding="gb18030") as f:
                    content = f.read()
            else:
                with codecs.open(src, mode="r", encoding=enc) as f:
                    content = f.read()
    except Exception as e:
        print("Error on %s %s" % (src, e))
    if content:
        return normalize_content(content) if clean else content


def convert_to_utf8(src, dst):
    try:
        content = read_content(src, clean=True)
        if content:
            with codecs.open(dst, mode="w", encoding="utf8") as f:
                f.write(content)
    except Exception as e:
        print("Error on %s %s" % (src, e))


def all_to_utf8(root):

    files = pathlib.Path(root).glob("**/*.txt")
    files = sorted(filter(lambda x: UTF8_SUFFIX not in str(x.parent), files))
    f_count = len(files)
    f_index = 0
    for file in files:
        f_index += 1
        src_file = pathlib.Path(file)
        src_dir = src_file.parent
        dst_dir = src_dir.with_stem("{}{}".format(src_dir.name, UTF8_SUFFIX))
        if not dst_dir.exists():
            dst_dir.mkdir()
        # 规范文件名，去掉特殊字符
        dst_name = normalize_filename(src_file.stem)
        dst_file = dst_dir.joinpath("{}{}".format(dst_name, src_file.suffix))
        if pathlib.Path(dst_file).exists():
            print("Skip: {}->{} ({}/{})".format(src_file, dst_name, f_index, f_count))
        else:
            print("toUTF8: {}->{} ({}/{})".format(src_file, dst_name, f_index, f_count))
            convert_to_utf8(src_file, dst_file)


if __name__ == "__main__":
    all_to_utf8(sys.argv[1])
