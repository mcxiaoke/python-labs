# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

'''
stat 模块定义了处理文件状态信息的常量和函数，一般使用 os.path.is**系列函数

stat.SF_APPEND      stat.S_ENFMT        stat.S_IRWXG        stat.S_IWRITE
stat.SF_ARCHIVED    stat.S_IEXEC        stat.S_IRWXO        stat.S_IWUSR
stat.SF_IMMUTABLE   stat.S_IFBLK        stat.S_IRWXU        stat.S_IXGRP
stat.SF_NOUNLINK    stat.S_IFCHR        stat.S_ISBLK        stat.S_IXOTH
stat.SF_SNAPSHOT    stat.S_IFDIR        stat.S_ISCHR        stat.S_IXUSR
stat.ST_ATIME       stat.S_IFIFO        stat.S_ISDIR    是否是目录       stat.UF_APPEND
stat.ST_CTIME       stat.S_IFLNK        stat.S_ISFIFO       stat.UF_COMPRESSED
stat.ST_DEV         stat.S_IFMT         stat.S_ISGID        stat.UF_HIDDEN
stat.ST_GID         stat.S_IFREG        stat.S_ISLNK        stat.UF_IMMUTABLE
stat.ST_INO         stat.S_IFSOCK       stat.S_ISREG    是否是普通文件        stat.UF_NODUMP
stat.ST_MODE        stat.S_IMODE        stat.S_ISSOCK   是否是Socket       stat.UF_NOUNLINK
stat.ST_MTIME       stat.S_IREAD        stat.S_ISUID        stat.UF_OPAQUE
stat.ST_NLINK       stat.S_IRGRP        stat.S_ISVTX
stat.ST_SIZE        stat.S_IROTH        stat.S_IWGRP
stat.ST_UID         stat.S_IRUSR        stat.S_IWOTH
'''

import os
from stat import *


def walk(root, callback):
    root = os.path.abspath(root)
    print "Start walking dir: %s" % root
    for f in os.listdir(root):
        pathname = os.path.join(root, f)
        mode = os.stat(pathname).st_mode
        print "file mode is %r" % mode
        if S_ISDIR(mode):
            # is dir
            walk(pathname, callback)
        elif S_ISREG(mode):
            # is regular file
            callback(pathname)
        else:
            # unknown type
            print 'Skipping %s ' % pathname


def visit(file):
    print 'Visiting regular file:', file


if __name__ == '__main__':
    walk('.', visit)
