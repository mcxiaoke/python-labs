# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 2015/7/7 21:39.
__author__ = 'mcxiaoke'

import shutil

# 高层文件和目录操作模块
# 注意：没办法复制所有的文件属性，比如owner和group会丢失,ACL会丢失

# 复制对象src到dst
# shutil.copyfileobj(fsrc, fdst[, length])

# 复制文件src到文件dst
# shutil.copyfile(src, dst)
# 注意：两个必须都是文件
# 仅复制内容，无元数据
# dst必须是完整的文件路径
# 如果src和dst是同一个文件，会抛异常
# 如果dst不可写，也会抛异常
# 如果dst已存在，会被替换掉
# src和dst都是代表文件路径的字符串

# 复制权限位
# shutil.copymode(src, dst)

# 复制修改时间和权限位等元数据
# shutil.copystat(src, dst)

# 复制文件src到dst
# shutil.copy(src, dst)
# src必须是文件，dst可以是文件，或目录
# 如果dst是目录，目标文件名会和src一致，权限位也会复制
# src和dst都是字符串

# 复制文件src到dst
# shutil.copy2(src, dst)
# 同shutil.copy()，但同时会复制元数据
# 等价于 copy+copystat()

# 创建ignore模式
# shutil.ignore_patterns(*patterns)
# 静态函数，用于创建供copytree使用的ignore参数(callable对象)

# 递归复制整个目录树
# shutil.copytree(src, dst, symlinks=False, ignore=None)
# src是原目录，dst是目标目录
# dst不能已经存在，会根据需要递归创建
# 元数据会使用copystat()复制，单独的文件使用copy2()复制
# symlinks，如果此参数为True，会复制符号链接，但是不会复制元数据
# ignore，如果有此参数，会根据条件过滤，返回一个需要过滤的文件路径序列
# 如果复制过程中发生了错误，会抛异常

# 递归删除目录树
# shutil.rmtree(path[, ignore_errors[, onerror]])
# path必须指向一个目录，不能是文件或者符号链接
# 如果ignore_errors=True，删除失败的操作会被忽略
# 如果操作失败，会调用onerror函数，如果没有指定onerror，会抛异常

# 移动文件
# shutil.move(src, dst)
# 递归的移动文件或目录到目的地
# 如果dst已存在且是一个目录，src会被移动到dst目录内
# 如果dst已存在但不是目录，会被覆盖，机制同os.rename()
# 如果dst和src在同一个文件系统，会调用os.rename()
# 如果dst和src不再同一个文件系统，会先复制src，再移除src

# 异常说明
# shutil.Error
# 文件操作会抛出异常，对于copytree()，异常的参数列表是三元组(srcname, dstname, exception).

# 辅助函数
# ignore_patterns
# 例子：copytree(source, destination, ignore=ignore_patterns('*.pyc', 'tmp*'))
# 也可以用来添加日志
'''
def _logpath(path, names):
    logging.info('Working in %s' % path)
    return []   # nothing will be ignored

copytree(source, destination, ignore=_logpath)
'''

# 创建压缩文件
# shutil.make_archive(base_name, format[, root_dir[, base_dir[,
# verbose[, dry_run[, owner[, group[, logger]]]]]]])
# basename 指定压缩文件的文件名，包括路径，不需要扩展名
# format 压缩文件格式，支持zip/tar/bztar/gztar四种
# root_dir 是压缩文件的根目录，默认是当前目录
# base_dir 压缩文件的起始目录，默认是当前你目录
# owner和group用于创建压缩文件，默认是当前用户和用户组
# logger 必须是一个PEP282兼容的Logger对象

# 压缩文件格式
# shutil.get_archive_formats()
# 返回支持的压缩文件格式，默认支持gztar.gzip/bztar.bzip2/tar/zip

# copytree()的实现示例
import os


def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
                # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise shutil.Error(errors)

# 压缩文件示例
'''
from shutil import make_archive
archive_name = os.path.expanduser(os.path.join('~', 'sshbackup'))
root_dir = os.path.expanduser(os.path.join('~', '.ssh'))
make_archive(archive_name, 'gztar', root_dir)
'''
