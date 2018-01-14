#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
from __future__ import print_function
import codecs
import os
import sys
import shutil
import re


def main():
    fin = os.path.abspath(sys.argv[1])
    fdir = os.path.dirname(fin)
    name = os.path.basename(fin)
    base, ext = os.path.splitext(name)
    fout = os.path.join(fdir, u"{}.md".format(base.decode('utf-8')))
    names = codecs.open(fin, 'r', 'utf-8').read().splitlines()
    with codecs.open(fout, 'w', 'utf-8') as f:
        for name in names:
            f.write(u'\n')
            f.write(u'## {}\n\n'.format(name))
            f.write(u'- 学名: 无\n')
            f.write(u'- 别名: 无\n')
            f.write(u'- 分类: 硬骨鱼纲/鲤形目/鲤科/鲤亚科\n')
            f.write(u'- 链接: <http://fishbase.org/summary/TODO>\n\n')
            f.write(u'![图片](photos/{}.jpg)\n\n'.format(name))
            f.write(u'TODO\n\n')
            f.write(u'### 形态特征\n\nTODO\n\n')
            f.write(u'### 生活习性\n\nTODO\n\n')
            f.write(u'------\n\n\n')


if __name__ == '__main__':
    main()
