#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-02-06 08:45:40
from __future__ import print_function
import os, sys, shutil, re

def backup(source, destination):
    pattern = r'(IMG)?_?(2016)(\d{2})(\d{2})_\w+\.(\w{3})'
    ip = re.compile(pattern)
    for name in os.listdir(source):
        pic = os.path.join(source,name)
        pic_size = os.stat(pic).st_size
        if os.path.isfile(pic):
            if pic_size <= 0:
                print('invalid:', pic)
                os.remove(pic)
                continue
            m = ip.match(name)
            if m:
                # img, year, month, day, ext
                # print(m.group(1),m.group(2),m.group(3),m.group(4),m.group(5))
                src = pic
                output = os.path.join(destination,m.group(2), m.group(3))
                if not os.path.exists(output):
                    os.makedirs(output)
                dst = os.path.join(output, name)
                # print('from:',src)
                # print('to:',dst)
                if not os.path.exists(dst):
                    #TODO copy file
                    print('Copied -> {}'.format(dst.encode('utf8')))
                    shutil.copy2(src,dst)
                # else:
                    # print('Ignore: ',dst)
            else:
                pass
        #         print('not matched:',name)

if __name__ == '__main__':
    SOURCE = u'E:\OneDrive\图片\本机照片'
    TARGET = u'E:\百度云同步盘\我的照片'
    backup(SOURCE, TARGET)
