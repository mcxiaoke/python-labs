# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 2015/7/8 21:17.
__author__ = 'mcxiaoke'

# 备份目录src到dst

import os, sys, shutil
from os import path


def ignore(dir, name):
    return False


def accepty_py_files(dir, name):
    _, ext = path.splitext(name)
    return not (ext and ext == '.py')


def copytree(src, dst, ignore=None, override=False):
    print('process dir: %s' % src)
    if not path.exists(src):
        print('dir %s not exists.' % src)
    else:
        if not path.exists(dst):
            os.makedirs(dst)
        for name in os.listdir(src):
            src_name = path.join(src, name)
            dst_name = path.join(dst, name)
            # print 'process %s' % src_name
            if ignore and ignore(src, name):
                print('ignore file: %s' % src_name)
            elif path.basename(src_name).startswith('.'):
                print 'ignore hidden: %s' % src_name
            elif path.isdir(src_name):
                copytree(src_name, dst_name)
            elif path.isfile(src_name):
                if path.exists(dst_name):
                    if override:
                        print('override file: %s' % src_name)
                        shutil.copy2(src_name, dst_name)
                    else:
                        print('ignore exists: %s' % src_name)
                        pass
                else:
                    print('backup file: %s' % src_name)
                    shutil.copy2(src_name, dst_name)
            else:
                print('ignore non-file: %s' % src_name)
    shutil.copystat(src, dst)


def expand_path(src, dst):
    if src.startswith('~'):
        src = path.expanduser(src)
    elif not path.isabs(src):
        src = path.abspath(src)
    if dst.startswith('~'):
        dst = path.expanduser(dst)
    elif not path.isabs(dst):
        dst = path.abspath(path.normpath(dst))
    if not path.basename(src) == path.basename(dst):
        dst = path.join(dst, path.basename(src))
    src = path.normcase(src)
    dst = path.normcase(dst)
    return (src, dst)


def backup(src, dst, accept=None, override=False):
    '''
    :param src: 源目录路径，完整路径或相对路径
    :param dst: 目标目录路径，完整路径或相对源目录的路径
    :param accept: 函数返回True才复制，否则不复制
    :param override: 是否覆盖目标目录已存在的文件，默认False
    :param logging: 是否记录操作日志，默认False
    :return: 返回未成功备份的文件列表
    '''
    src, dst = expand_path(src, dst)
    print 'src: %s' % src
    print 'dst: %s' % dst
    # copytree(src, dst, override=True)


def test_backup():
    src = '..'
    dst = path.join('..', '..', 'backup')
    backup(src, dst)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: python %s source_dir target_dir" % path.basename(sys.argv[0])
        sys.exit(1)
    backup(sys.argv[1], sys.argv[2])
