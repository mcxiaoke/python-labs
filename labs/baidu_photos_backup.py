#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

from backup_photos_by_date import backup, copy_by_date

# 百度照片按日期整理脚本
SRC = u'E:\Sync\Xiaoke\'s iPhone\Photo'
SRC2 = u'E:\TempPhotos'
DST = u'E:\百度云同步盘\我的照片'
BACKUP = u'E:\Tools\GoogleBackup\Photos'
#BACKUP = u'E:\Temp'
SINCE = '20180701'
    
if __name__ == '__main__':
    print(sys.argv)
    dry_run = len(sys.argv) == 2 and sys.argv[1] == '-n'
    print(dry_run)
    copy_by_date(SRC2, DST, SINCE)
    copy_by_date(SRC, BACKUP, SINCE)
