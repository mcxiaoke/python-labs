#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

from backup_photos_by_date import backup, copy_by_date

# 百度照片按日期整理脚本

DST = u'E:\百度云同步盘\我的照片'
BACKUP = u'E:\Tools\GoogleBackup\Photos'
#BACKUP = u'E:\Temp'
SINCE = '20180410'
    
if __name__ == '__main__':
    print(sys.argv)
    dry_run = len(sys.argv) == 2 and sys.argv[1] == '-n'
    print(dry_run)
    SRC = u'E:\百度云同步盘\来自：iPhone'
    backup(SRC, DST, dry_run)
    copy_by_date(SRC, BACKUP, SINCE)
    SRC = u'E:\百度云同步盘\来自：iPad'
    backup(SRC, DST, dry_run)
    copy_by_date(SRC, BACKUP, SINCE)
    SRC = u'E:\百度云同步盘\来自：SM-N9100'
    backup(SRC, DST, dry_run)
    copy_by_date(SRC, BACKUP, SINCE)
