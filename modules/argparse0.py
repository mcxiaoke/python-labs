# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/6 08:07.
__author__ = 'mcxiaoke'

import os, sys

# 命令行参处理
# Python 2.7.6 (default, Nov 10 2013, 19:24:18) [MSC v.1500 32 bit (Intel)] on win32

import argparse

parser = argparse.ArgumentParser()
# 默认会添加 -h/--help 的命令行参数解析
'''
>python argparse0.py --help
usage: argparse0.py [-h]
optional arguments:
  -h, --help  show this help message and exit

>python argparse0.py hello
usage: argparse0.py [-h]
argparse0.py: error: unrecognized arguments: hello
'''


# parser.add_argument('echo')
# args = parser.parse_args()
# print  'args:', args.echo
# 最简单的参数
'''
>python argparse0.py echo
args: echo
'''

# parser.add_argument('echo',help='echo the text what you use here.')
# args=parser.parse_args()
# print args.echo
# 参数的帮助文档
'''
>python argparse0.py -h
usage: argparse0.py [-h] echo
positional arguments:
  echo        echo the text what you use here.
optional arguments:
  -h, --help  show this help message and exit
'''

# parser.add_argument('square', help='display a square of a given number', type=int)
# args = parser.parse_args()
# print args.square ** 2
# 指定参数的类型，此时参数名只是个代号
'''
>python argparse0.py 5
25
>python argparse0.py five
usage: argparse0.py [-h] square
argparse0.py: error: argument square: invalid int value: 'five'
'''

# parser.add_argument('--verbosity', help='increase output verbosity')
# args = parser.parse_args()
# if args.verbosity:
#    print 'verbosity turned on.'
# 可选参数，没有传参时不报错
'''
>python argparse0.py --verbose 1
verbosity turned on.
>python argparse0.py --help
usage: argparse0.py [-h] [--verbose VERBOSITY]
optional arguments:
  -h, --help            show this help message and exit
  --verbose VERBOSITY
                        increase output verbosity
'''

# parser.add_argument('-v','--verbose', help='increase output verbosity', action='store_true')
# args = parser.parse_args()
# if args.verbosity:
#    print 'verbosity turned on.'
# 指定长短参数，参数值为布尔类型，如果指定了参数，值为True，默认为False
'''
>python argparse0.py --verbose 1
usage: argparse0.py [-h] [-v]
argparse0.py: error: unrecognized arguments: 1
>python argparse0.py --verbosity
verbosity turned on.
>python argparse0.py -h
usage: argparse0.py [-h] [-v]
optional arguments:
  -h, --help       show this help message and exit
  -v, --verbose  increase output verbosity
'''

# 此时例子的完整代码
# source
'''
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square ** 2
if args.verbose:
    print "the square of {} equals {}".format(args.square, answer)
else:
    print answer
'''
# usage
'''
>python argparse0.py
usage: argparse0.py [-h] [-v] square
argparse0.py: error: too few arguments
>python argparse0.py -h
usage: argparse0.py [-h] [-v] square
positional arguments:
  square         display a square of a given number
optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
>python argparse0.py 5
25
>python argparse0.py 5 --verbose
the square of 5 equals 25
'''

# 参数值处理
# source
'''
parser = argparse.ArgumentParser()
parser.add_argument('square', type=int,
                    help='display a square o a given number')
parser.add_argument('-v', '--verbose', type=int,
                    help='increase output verbosity')
args = parser.parse_args()
answer = args.square ** 2
if args.verbose == 2:
    print 'the square of {} is equals {}'.format(args.square, answer)
elif args.verbose == 1:
    print '{}^2=={}'.format(args.square, answer)
else:
    print answer
'''
# usage
'''
>python argparse0.py 5
25
>python argparse0.py 5 --verbose=1
5^2==25
>python argparse0.py 5 --verbose=2
the square of 5 is equals 25
>python argparse0.py 5 -v=3
25
>python argparse0.py -h
usage: argparse0.py [-h] [-v VERBOSE] square
positional arguments:
  square                display a square o a given number
optional arguments:
  -h, --help            show this help message and exit
  -v VERBOSE, --verbose VERBOSE
                        increase output verbosity
'''

# 以下部分开始使用Python 2.7.10版本

# 数字求和
# source
'''
# 构造方法可以指定一个说明文字
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')
# parse_args()方法用于解析参数，默认从sys.argv读取参数列表
args = parser.parse_args()
print args.accumulate(args.integers)
'''
# usage
'''
>python argparse0.py 1 2 3 5 --sum
11
>python argparse0.py 1 2 3 5
5
>python argparse0.py a b c
usage: argparse0.py [-h] [--sum] N [N ...]
argparse0.py: error: argument N: invalid int value: 'a'
>python argparse0.py
usage: argparse0.py [-h] [--sum] N [N ...]
argparse0.py: error: too few arguments
>python argparse0.py -h
usage: argparse0.py [-h] [--sum] N [N ...]
Process some integers.
positional arguments:
  N           an integer for the accumulator
optional arguments:
  -h, --help  show this help message and exit
  --sum       sum the integers (default: find the max)
'''

# 构造方法原型
# class argparse.ArgumentParser(
# prog=None, # 脚本的名字，默认值是sys.argv[0]
# usage=None, # 使用方法说明，默认从参数列表生成
# description=None, # 参数描述
# epilog=None, # 显示在帮助文档之后的文本
# parents=[], #  ArgumentParser对象列表
# formatter_class=argparse.HelpFormatter, # 自定义帮助文档输出格式
# prefix_chars='-', # 可选参数默认前缀，默认是'-'
# fromfile_prefix_chars=None, # 从文件读取额外参数
# argument_default=None, # 默认参数
# conflict_handler='error', # 可选参数冲突处理器
# add_help=True) # 是否添加默认的 -h/--help参数

# prog
# parser = argparse.ArgumentParser()
# parser.print_help()
'''
usage: argparse0.py [-h] #默认使用的是文件的名字
optional arguments:
  -h, --help  show this help message and exit
'''
# parser = argparse.ArgumentParser(prog='hello')
# parser.print_help()
'''
usage: hello [-h] #现在的名字是'hello'了
optional arguments:
  -h, --help  show this help message and exit
'''

# usage
# parser = argparse.ArgumentParser(prog='hello',usage='%(prog)s [options] (hello, world)')
# parser.print_help()
'''
usage: hello [options] (hello, world)
optional arguments:
  -h, --help  show this help message and exit
'''

# description
# parser = argparse.ArgumentParser(prog='hello',
#                                  description='this is usage description.',
#                                  epilog='this is some text after usage')
# parser.print_help()
'''
usage: hello [-h]
this is usage description.
optional arguments:
  -h, --help  show this help message and exit
this is some text after usage
'''

# parents
'''
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--parent', type=int, help='parent parser index.')
parser = argparse.ArgumentParser(prog='hello', parents=[parent_parser])
parser.add_argument('k')
print parser.parse_args(['--parent', '2', 'xxx'])  # Namespace(parent=2, x='xxx')
parser = argparse.ArgumentParser(prog='hello', parents=[parent_parser])
print parser.parse_args()  # Namespace(parent=None)
'''

# formatter_class
'''
有三种格式：
argparse.RawDescriptionHelpFormatter #description和epilog是已经正确格式化了，不需要折行
argparse.RawTextHelpFormatter #不过滤空白字符，包括参数的描述
argparse.ArgumentDefaultsHelpFormatter # 会给每个参数添加默认的描述信息
'''

#prefix_chars
# 自定义参数前缀
parser = argparse.ArgumentParser(prog='hello',prefix_chars='-+_')
parser.add_argument('+m')
parser.add_argument('-n')
parser.add_argument('_p')
print parser.parse_args('+m X -n Y _p Z'.split()) #Namespace(m='X', n='Y', p='Z')

#TODO 15.4.2.8. fromfile_prefix_chars