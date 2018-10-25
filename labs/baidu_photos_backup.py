#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

from backup_photos_by_date import backup, copy_by_date

# 百度照片按日期整理脚本
SRC = u'E:\TempPhotos'
SRC2 = u'D:\Baidu\iPhone'
DST = u'E:\照片备份\手机照片'
SINCE = '20180501'
    
if __name__ == '__main__':
    print(sys.argv)
    dry_run = len(sys.argv) == 2 and sys.argv[1] == '-n'
    print(dry_run)
    backup(SRC, DST) # by name pattern 
    backup(SRC2, DST)
    #copy_by_date(SRC, BACKUP, SINCE) # by modify time
    
# copy photos from to E:\TempPhotos
# python image_exif_rename.py E:\TempPhotos
# python backup_photos_by_date.py E:\照片备份\手机照片
