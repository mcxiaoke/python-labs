#-*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

'''
os.path用于处理文件路径，但它只是path模块的一个别名，对应的各个系统的具体实现是posixpath/ntpath/macpath等
os.path.abspath(path) 获取对应路径的绝对路径，会对.和..这类相对路径展开，这个函数不检查路径是否真实存在
os.path.basename(path) 返回路径最后的基本名字，如 /some/path/返回''，some/path/name返回'name'，这个函数也不检查路径是否真实存在，只是字符串处理
os.path.dirname(path) 返回的和os.path.basename剩余的部分，如/some/path返回some，some/path/返回some/path
os.path.exists(path) 判断路径是否在文件系统中真实存在，如果没有权限读取也会返回False
os.path.expanduser(path) 展开带用户目录~的路径，忽略不是以~开头的路径，在windows下一版是 C:\\Users\someone\xxx，在Linux下一版是 /home/someone/xxx
os.path.expandvars(path) 展开带环境变量的路径，格式为${ENV}，如${JAVA_HOME}会展开为类似于这样的绝对路径'C:\\Program Files\\Java\\jdk1.7.0_60'
os.path.getatime(path)获取文件的最近访问时间，如果文件不存在或没有权限会抛出异常，类似的的函数还有getmtime(path)获取最近修改时间，getctime(path)获取文件元数据修改时间
os.path.getsize(path) 获取文件大小，如果不存在或没有权限会抛出异常
其他的实用函数还有
path.isabs(path) 是否是绝对路径
path.isfile(path) 是否是普通文件，包含软链接
path.isdir(path) 是否是目录，包含软链接
os.islink(path) 是否是软链接
os.path.join(path1,path2...) 拼接路径，如果任何一个是绝对路径，之前的会被丢弃，如 os.path.join('hello','/world','some','test.txt')返回'/world/some/test.txt'，如果最后一个路径是空，会自动添加一个分隔符，如 os.path.join('/usr/local','some','path','')返回'/usr/local/some/path/'，要注意的是，在Windows上这个会返回盘符和当前目录，不是绝对路径
os.path.normcase(path) 规范化路径名，在不区分大小写的文件系统，它返回小写路径名，在Windows上会将'/'转换为'\\'，如os.path.normcase('/hello/world')会返回'\\hello\\world'
os.path.normpath(path) 规范化路径名，例子：A//B, A/B/, A/./B和A/foo/../B返回的结果都是A/B
os.path.realpath(path) 返回真实路径，会跟随软链接，.和..都会被展开，类似的还有os.path.relpath会返回相对路径
os.path.samefile(path1, path2)  是否同一个文件
os.path.sameopenfile(fp1, fp2) 两个文件描述符是否指向同一个文件
os.path.split(path) 分割路径为dirname和basename，如os.path.split('some/path/here')返回('some/path', 'here')，os.path.split('some/path/here/')返回('some/path/here', '')
os.path.splitdrive(path) 分割路径为盘符和路径，如os.path.splitdrive('C:\\Pythons\libs')返回('C:', '\\Pythons\\libs')
os.path.splitext(path) 分割路径为路径和扩展名，如os.path.splitext('C:\\Python\libs\hello.txt')返回('C:\\Python\\libs\\hello', '.txt')，而os.path.splitext('C:\\Python\libs\somedir')返回('C:\\Python\\libs\\somedir', '')
os.path.splitunc(path) 这个不清楚做什么用的
os.path.walk(path, visit, arg) 使用visit函数遍历路径，函数参数为(arg, dirname, names)，dirname表示当前正在处理的目录，names表示此目录下的文件，这个函数不跟随软链接，例子：
'''

import os

def process(arg,dirname,names):
    dir_path=os.path.join(dirname,dirname)
    print ("processing dir:%s" % dir_path)
    for file in names:
        file_path=os.path.join(dirname,file)
        print "processing file:%s" %file_path

os.path.walk('libs',process,())

# os.path.supports_unicode_filenames 一个属性，返回操作系统是否 支持Unicode文件名



















