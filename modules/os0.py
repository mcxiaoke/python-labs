# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

'''
os模块提供操作系统相关的功能，如果你只是想读写文件，使用open()更方便，
操作路径可以使用os.path，按行读取文件可以使用fileinput，
创建临时文件可以使用tempfile，高层文件和目录处理可以使用shutil
'''

import os

print os.name  # 返回os模块对应的实际模块名字
# out: 'posix', 'nt', 'os2', 'ce', 'java', 'riscos'
# print os.environ #返回系统的所有环境变量
os.environ['TMP']
# out: '/var/folders/53/n994f2492dz6zx4f6x812xvh0000gp/T/'
# 可以使用 putenv() unsetenv() 修改环境变量

os.getgid()  # 获取当前进程的用户组
os.getgroups()  # 获取与前挡进程关联的用户组列表
os.getlogin()  # 获取当前登录用户的帐号名
os.getuid()  # 获取当前进程的UID
os.getpid()  # 获取进程PID
os.getpgrp()  # 获取进程GROUP
os.getppid()  # 获取父进程PID

os.getenv('JAVA_HOME')  # 获取某个环境变量的值
# out: '/Library/Java/JavaVirtualMachines/jdk1.7.0_55.jdk/Contents/Home'
os.strerror(1)  # 返回错误码对应的错误消息
os.strerror(1)  # out: 'Operation not permitted'
os.strerror(2)  # out: No such file or directory'
# some error codes/messages
# for i in range(100):
#    print i,":",os.strerror(i)

print os.uname()[0]  # 获取五元组，用于标识当前操作系统
# (sysname, nodename, release, version, machine)
# out: ('Darwin', 'mcmbp.local', '14.4.0',
# 'Darwin Kernel Version 14.4.0: Thu May 28 11:35:04 PDT 2015;
# root:xnu-2782.30.5~1/RELEASE_X86_64', 'x86_64')

# os.fdopen() # 打开文件描述符，mode必须以'r','w','a'之一开头
os.tmpfile()  # 打开一个临时文件，返回file对象，默认模式是w+b，无目录信息，会自动删除

# 以下是文件描述符相关的操作
# os.close(fd) 关闭fd
# os.dup(fd) 复制fd
# os.dup2(fd,fd2) 复制fd到fd2
# os.fchmod(fd,mode)
# os.fstat(fd) 同stat()
# os.open(file,flags,mode) 打开文件，返回文件描述符int
# os.pipe() # 打开双向管道，返回(r,w)元组
# os.read(fd, n) # 从fd指向的文件中读取至多n个字节，返回一个字符串
# os.write(fd, str) # 向fd指向的文件写入字符串

# 以下是文件和目录相关的操作
os.access('.', os.R_OK)  # 测试对此文件是否有指定的权限
# 读 R_OK/ 写 W_OK/ 执行 X_OK/ 存在 F_OK
def test_read():
    if os.access('stat0.py', os.R_OK):
        with open('stat0.py') as fp:
            print "access file ", fp.name
            return fp.read()
    return "file can not read"

# print test_read()

# os.chdir('/var/tmp')  # 改变当前目录
os.getcwd()  # 获取当前目录的路径
os.getcwdu()  # 获取当前目录，返回Unicode对象
# os.chroot('/var/tmp')  # 改变当前进程的根目录
# os.chmod('os0.py',777) # 改变某个路径的权限模式
# os.chown(path, uid, gid) # 改变用GID和UID
os.listdir('.')  # 获取目录下的项目列表，不包括.和..
# out: ['file_input.py', 'os0.py', 'os_path.py', 'stat0.py', 'temp_file.py']
# os.mkdir('some_dir', 777)  # 创建目录
# os.makedirs('one/two/thress')  # 递归创建多层目录
# os.rename(src,dst) # 重命名，dst不能是目录
# os.renames(old,new) #重命名，递归操作
# os.remove('some_file')  # 删除某个文件，不支持目录
# os.removedirs('some_dir')  # 递归删除某个目录
# os.rmdir('one')  # 删除某个目录
# os.symlink(source, link_name) # 穿件一个符号链接

# os.utime(path, times) # 设置给定文件的访问和修改时间

os.stat('.')  # 获取文件属性，等同于stat()系统调用
# out: osix.stat_result(
# st_mode=16877,
# st_ino=141459662,
# st_dev=16777220L,
# st_nlink=12,
# st_uid=502,
# st_gid=20,
# st_size=408,
# st_atime=1435937839,
# st_mtime=1435937875,
# st_ctime=1435937875)

os.statvfs('.')  # 获取文件系统属性，等同于statvfs()系统调用
# out: osix.statvfs_result(f_bsize=1048576, f_frsize=4096,
# f_blocks=60978816, f_bfree=34845049, f_bavail=34781049,
# f_files=60978814, f_ffree=34781049, f_favail=34781049,
# f_flag=0, f_namemax=255)

# 遍历目录
# os.walk(top, topdown=True, onerror=None, followlinks=False)
for root, dirs, files in os.walk('.'):
    print "process ", os.path.abspath(root),
    print sum(os.path.getsize(os.path.join(root, name)) for name in files),
    print "bytes in", len(files), " regualr files"

# Delete everything reachable from the directory named in "top",
# assuming there are no symbolic links.
# CAUTION:  This is dangerous!  For example, if top == '/', it
# could delete all your disk files.
'''
import os
for root, dirs, files in os.walk(top, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
'''

# 15.1.5. Process Management
os.execv('/bin/ls', ['-a', '-l'])  # 需要使用绝对路径
# 发送SIGABRT信号给当前进程，调用这个函数不会触发Python的SIGABRT信号处理器
os.abort()
'''
# 这系列函数都是执行外部程序，加载进当前进程，
# 在Unix上，这个函数替换当前进程，不会改变进程PID
# 当前进程会被立即替换，打开的文件和描述符缓存不会刷新和回写
# 带p的函数会使用PATH环境变量加载外部可执行文件
os.execl(path, arg0, arg1, ...)
os.execle(path, arg0, arg1, ..., env)
os.execlp(file, arg0, arg1, ...)
os.execlpe(file, arg0, arg1, ..., env)
os.execv(path, args)
os.execve(path, args, env)
os.execvp(file, args)
os.execvpe(file, args, env)
'''
# os.fork() 创建一个子进程，在child进程中返回0，在parent进程中返回子进程的PID
# os.kill(pid,sig) # 发送信号给指定进程
# os.killpg(pgid, sig) # 发送信号给指定进程组
print os.system("ls -a")  # 等同于调用C语言的system()
os.times()  # 返回一个代表时间的五元组，分别是
# user time,
# system time,
# children’s user time,
# children’s system time,
# and elapsed real time since a fixed point in the past
# out: (0.19, 0.04, 0.0, 0.0, 1435990863.13)

# os.wait() # 等待子进程结束
# os.waitpid(pid, options) # 等待进程结束
# 几个实用变量，更多功能可用path模块
# os.curdir, os.pardir, os.sep, os.altsep
# os.extsep, os.pathsep, os.linesep, os.devnull
os.urandom(10)  # 返回一个N字节的随机字符串，一般用于加密
