# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/5 10:22.
__author__ = 'mcxiaoke'

# 内置函数 Built-in Functions

# 取绝对值
print abs(-100)  # 100
print abs(-3.1415926)  # 3.1415926
print abs(0xff)  # 255

# 检查是否所有值为真
'''
def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True

'''
print all([1, 2, 3])  # out:True
print all(['', 'hello', 123])  # out:False
print all([0, 1, 2, 3])  # out:False

# 检查是否有任何一个值为真
'''
def any(iterable):
    for element in iterable:
        if element:
            return True
    return False
'''
print any(['', 'hello', 123])  # out:True
print any([0, 1, 2, 3])  # out:True
print any(['', 0, 0.0, False, None, [], {}, ()])  # out:False
print any([[], [], []])  # out:False

# 整数-->二进制字符串
print bin(1234)  # 0b10011010010
print bin(0xff)  # 0b11111111

# 转换为布尔值
print bool([])  # out:False
print bool(None)  # out:False
print bool('')  # out:False
print bool(0.0)  # out:False
print bool(['hello'])  # out:True
print bool(1234)  # out:True
print bool(3.14)  # out:True
print bool('world')  # out:True

# 字节数组
data = bytearray('hello,world')
print data  # out:hello,world

# 是否可执行
print callable(bin)  # True
print callable('hello')  # False

# ASCII字符
print chr(34), chr(54), chr(94)  # " 6 ^
# for i in range(0, 127):
#    print i, ':', chr(i),

# 返回一个类方法
# classmethod(func)
# @classmethod 函数装饰器
'''
class C(object):
    @classmethod
    def f(cls, arg):
        print cls.__name__, arg
C.f('hello')  # C hello
C().f('hello')  # C hello
'''

# 比较大小
# cmp(x, y) 如果x>y，返回正数，如果x<y，返回负数，如果相等返回0
print cmp(0.52, 0.52)  # 0
print cmp(3.0, 3)  # 0
print cmp(100, 200)  # -1
print cmp(999, 3.14)  # 1
print cmp('hello', 'world')  # -1
print cmp('A', 234)  # 1

# 编译源码
# compile(source, filename, mode[, flags[, dont_inherit]])
# mode = exec|eval|single
code = compile("print bin(1234)", 'file_name', 'exec')
print repr(code.co_code)  # out:'e\x00\x00d\x00\x00\x83\x01\x00GHd\x01\x00S'
exec code  # out: 0b10011010010
eval(code)  # out: 0b10011010010

# 创建复数
# complex([real[, imag]])
print complex(123, 200)  # (123+200j)
print complex('1+2j')  # (1+2j)

# 设置属性
# setattr(object, name, value)
# 检测属性
# hasattr(object, name)
# 删除属性
# delattr(object, name)
# 获取属性
# getattr(object, name[, default])
'''
class A(object):
    def __init__(self):
        self.x = 100
        self.y = 200
a = A()
setattr(a, 'x', '1234')
setattr(a, 'z', 'hello_a')
print 'x=%s, y=%s, z=%s' % (a.x, a.y, a.z)  # out:x=1234, y=200, z=hello_a
print getattr(a, 'z')  # hello_a
delattr(a, 'x')
print hasattr(a, 'y'), hasattr(a, 'x')  # out: True False
# getattr(a, 'x')  # AttributeError: 'A' object has no attribute 'x'
# a.x # AttributeError: A instance has no attribute 'x'
'''

# 创建字典
# dict(**kwarg)
# dict(mapping, **kwarg)
# dict(iterable, **kwarg)

# 对象属性列表
# dir([object]) 从__dir__()/__dict()__取值
# 如果object是一个module，返回module的属性列表
# 如果object是一个type或class，返回属性列表，包括基类的属性
# 对于其它类型，返回属性列表
'''
class A(object):
    def __init__(self):
        self.x = 100
        self.y = 200

    def hello(self):
        print 'hello, world!'

    def __dir__(self):
        dirs = [x for x in self.__dict__ if not x.startswith('__')]
        return dirs + ['key1', 'key2']
a = A()
print dir(a)  # ['key1', 'key2', 'x', 'y']
'''
# 当前模块命名空间的属性列表
print dir()
# out: ['__author__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'code', 'data']

# 取模
# divmod(a, b) 返回一个元组  (a // b, a % b)
print divmod(10, 3)  # (3, 1)

# 创建枚举
# enumerate(sequence, start=0)
e = enumerate(['hello', 'world', 'cat', 'dog'])
print e.next(), e.next(), e.next()  # out: (0, 'hello') (1, 'world') (2, 'cat')
print list(e)  # out:[(0, 'hello'), (1, 'world'), (2, 'cat'), (3, 'dog')]
# 等价于
'''
def enumerate(sequence, start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n += 1
'''

# 执行表达式
# eval(expression[, globals[, locals]])
# 表达式必须是Unicode或Latin-1字符串，globals或locals需要是一个dict
# 这个函数可以执行任意code对象(包括compile()创建的)
x = 3
print eval('x ** 3')  # 27
# print eval('print bin(1234)') # SyntaxError: invalid syntax

# 执行代码
# execfile(filename[, globals[, locals]])
# 类似于exec，从文件读取，但不创建新的module
# execfile('execfile_test.py')  # out: hello execfile test output

# 创建文件对象
# file(name[, mode[, buffering]]) 建议使用open()函数
f = file('hello.txt', 'w')

# 序列过滤
# filter(function, iterable) 支持可迭代的数据
# 用function返回True的元素构建一个新的序列
# 如果function不是None，等价于[item for item in iterable if function(item)]
# 如果function==None，等价于[item for item in iterable if item]
print filter(None, [0, "", 'hello', 3.14, 100, []])  # out:['hello', 3.14, 100]
print filter(str.isupper, ['ABC', 'Hello', 'cat', 'CLASS'])  # out:['ABC', 'CLASS']

# 转换为float
# float([x]) 字符串或数字转换为一个浮点数
print float(-2015), float('3.14  ')  # out: -2015.0 3.14
# float('abc2.58xyz') # out: ValueError: could not convert string to float: abc2.58xyz

# 格式化表示
# format(value[, format_spec])
# format(value, format_spec) 内部调用 value.__format__(format_spec)

# 不可变set
# frozenset([iterable])
st = {1, 353, 56, 71, 400}
st.add(2015)
fs = frozenset(st)
# fs.remove(2015) # AttributeError: 'frozenset' object has no attribute 'remove'


# 全局符号表
# globals() 返回当前模块的全局符号表一个字典
globals()

# 对象的哈希值
# hash(object) 用于字典key的比较和查找
hash('hello')  # Out[88]: 840651671246116861
hash(12345)  # Out[89]: 12345
hash(3.14)  # Out[90]: 3146129223

# 帮助文档
# help([object]) 调用内置的帮助系统
# help(bin),help('os'),help(str.isupper)

# 十六进制字符串
# hex(x) 整数值转换为16进制字符串，如果对象定义了__index__()，也支持
print hex(-65535)  # out:-0xffff
# hex(3.1415926) #out: TypeError: hex() argument can't be converted to hex

# 内存地址(指针)
# id(object)，同一对象的id在生命周期内保持不变
print id('hello')  # 4397064080
print id([1, 2, 3])  # 4550260136

# 输入并解释
# input([prompt]) 等价于 eval(raw_input(prompt)).

# 转换为int
# int(x=0)
# int(x, base=10)
# 转换为long
# long(x=0)
# long(x, base=10)
print int(123.029)  # 123
print int('2015')  # 2015
print hex(int('0xcca0', 16))  # 0xcca0

# 检测对象类型
# isinstance(object, class|type) 判断是类的实例或子类
# issubclass(class, classinfo) 是否是子类
print isinstance(123456, int)  # True
print isinstance(123456, float)  # False
print isinstance('123456', str)  # True
print isinstance('123456', int)  # False

# 迭代器对象
# iter(o[, sentinel])
# 如果第二个是终止标志，第一个参数是一个callable对象
'''
with open('data.txt') as fp:
    for line in iter(fp.readline, ''):
        process_line(line)
'''

# 对象的长度
# len(s) 对象必须是一个序列或一个集合
# len(12345)  # TypeError: object of type 'int' has no len()
print len('12345')  # out:5

# 创建列表
# list([iterable]) 从可迭代序列或迭代器创建可变列表
print list((1, 2, 3, 4, 5))  # out:[1, 2, 3, 4, 5]
print list(range(1, 10, 2))  # out:[1, 3, 5, 7, 9]
print list('hello')  # out:['h', 'e', 'l', 'l', 'o']
print list(u'cat,dog ')  # out:[u'c', u'a', u't', u',', u'd', u'o', u'g', u' ']

# 本地符号表
# locals() 不应该修改返回的字典
'''
class AA(object):
    def __init__(self):
        self.x = 123

    def hello(self):
        x = 100
        cat = 'lovely cat'
        print x, cat
        print hash(self), locals()
AA().hello() # {'x': 100, 'self': <__main__.AA object at 0x1072ff610>, 'cat': 'lovely cat'}
'''

# 应用函数到序列
# map(function, iterable, ...) 返回结果是一个list
print map(lambda x: x ** 3, [1, 2, 3, 4])  # out:[1, 8, 27, 64]
print map(str.upper, ['hello', 'world', 'value'])  # out:['HELLO', 'WORLD', 'VALUE']

# 最大值和最小值
# max(iterable[, key])
# max(arg1, arg2, *args[, key])
# min(iterable[, key])
# min(arg1, arg2, *args[, key])
print min([1, 2, 3, 4, 5])  # out:1
print min(xrange(1, 4, 9))  # out:1
print max(('hello', 'world', 'cat', '123'))  # out:'world'
print max(range(1, 100))  # out:99

# 迭代器next()函数
# next(iterator[, default]) 返回迭代器的下一个对象
it = iter([1, 2, 3, 4, 5, 6, 7, 8])
print type(it)  # out:<type 'listiterator'>
print next(it), next(it), next(it)  # out:1 2 3

# 八进制数
print oct(10000)  # 023420
print oct(0xffff)  # 0177777
# 计算幂
# pow(x, y[, z]) # 计算x的y次方，z为取模，两个参数时等价于 x**y
print pow(3, 4)  # out:81
print pow(2, 8)  # out:256
print pow(2, 8, 10)  # out:6

# 返回ASCII码
print ord('a'), ord('A'), ord('8')  # out:97 65 56
# 返回ASCII字符
print chr(97), chr(65), chr(56)  # out:a A 8

# 打开文件
# open(name[, mode[, buffering]]) 打开文件
# 具体用法见 builtin_file.py
# r模式用于读，不能写
# w模式用于写，如果文件已存在，会清空内容
# a模式用于追加
# 默认模式是r
# buffering指定缓冲区大小，0=不缓冲，1=行缓冲，其它值=精确的缓冲区大小
# 这三种模式(带+号)可以读和写 'r+', 'w+', 'a+'

# 打印对象到流文件
# 2.6版python增加的函数
# 默认打印到标准输出，默认分隔符是空格，默认结束符是'\n'
# print(*objects, sep=' ', end='\n', file=sys.stdout)
# f = open('hello.txt', 'w+')
print([1, 2, 3, 4, 5])  # out:[1, 2, 3, 4, 5]

# 读取属性
# property([fget[, fset[, fdel[, doc]]]])
