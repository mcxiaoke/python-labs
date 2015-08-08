#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-08 21:40:22
from __future__ import print_function
from Tkinter import *
import sys


# 第一个例子
'''
1. 从Tkinter模块加载一个控件类
2. 创建导入的这个类的实例
3. 将Label包装到父控件
4. 开始事件循环

GUI都是事件驱动编程
mainloop内部监听键盘和鼠标等用户事件
# 创建这个控件的实例
# 第一个参数表示需要附着的父控件对象，传入None表示附着到应用的顶层窗口
# 第二个参数text表示Label上显示的文本内容
# 大部分控件都接受键值对形式的多个参数，如text,color,size,callback等等
# gui1.py
widget=Label(None,text='Hello, GUI World!')
# 如果没有这一句tk的图形管理器就无法知道控件的存在，只会显示一个空窗口
# 使用packer图形管理器
widget.pack()
# 如果没有这一句事件循环不会开始，不会进入等待状态，不会有窗口出现
widget.mainloop()
'''

# 图形管理器
'''
pack方法调用图形管理器，用于控制窗口控件的排列方式（布局）
# gui1c.py
root=Tk()
# 默认就是TOP
Label(root,text='Hello GUI World!').pack(side=TOP)
root.mainloop()
'''

# packer图形管理器给每个控件分配能容纳它的内容的空间大小
# expand=YES 表示扩展父容器中的可用空间
# fill 选项表示缩放时可用空间的扩展方向，选项X/Y/BOTH
# gui1e.py
'''
Label(text='Hello World').pack(expand=YES, fill=BOTH)
mainloop()
'''

# 设置属性
'''
root=Tk()
widget=Label(root)
# 加个背景色可以看出expand和FILL参数的效果
widget['bg']='gray'
#widget['text']='Hello, GUI World!'
# config 方法可以在任何时候调用，即时改变控件的样式，动态配置
widget.config(text='Hello, GUI World!')
#widget.pack(side=TOP)
# 注意：pack()方法返回None，不能这样用
# Label(text='Hi').pack().mainloop()
widget.pack(side=TOP,expand=YES,fill=X)
# 还可以这样批量传参数，但是不建议使用
# options={'text':'hello, world'}
# layout={'side','top'}
# Label(None,**options).pack(**layout)
root.title('GUI')
mainloop()
'''

# 添加事件回调
# command指定点击Button时的事件处理器函数
'''
widget=Button(None,text='Hello widget world',command=sys.exit)
widget.pack()
widget.mainloop()
'''
'''
root = Tk()
Button(root, text='Press', command=root.quit).pack(
    side=LEFT, expand=YES, fill=X)
#Button(root,text='Button',command=root.quit).pack(side=RIGHT, expand=YES)
root.mainloop()
'''

# 自定义事件处理器
# custom callback handler
# callback可以是任意的 callable 对象，或者定义了 __call__ 操作的对象
'''
def quit():
    print "I must be going..."
    sys.exit()

widget=Button(None,text='Press to Quit',command=quit)
widget.pack()
widget.mainloop()
'''

# lambda回调
'''
# 使用 or 让两个函数都可以执行
widget = Button(None, text='Hello lambda!',
                command=(lambda:
                         print('lambda, I must be going...') or sys.exit()))
widget.pack()
widget.mainloop()
'''

'''
# lamda的技巧，可以推迟函数的执行
# Button的callback默认没有参数
# 下面是传递额外参数的方法
def handler(name):
    print('hello, your name is %s' % name)
root=Tk()
# 这个会立即执行，这种用法是错误的
Button(root,text='Button1', command=handler('run')).pack()
# 这样参数不对，会报错
# TypeError: handler() takes exactly 1 argument (0 given)
Button(root,text='Button2', command=handler).pack()
# 这个会推迟defer执行
Button(root,text='Button3', command=(lambda: handler('defer'))).pack()
def temp():
    handler('temp')
# 或者这样也可以
Button(root,text='Button4', command=temp).pack()
root.mainloop()
# 也可以这样传递参数
def makegui():
    X = 42 # X is retained auto 
    Button(text='ni', command=(lambda: handler(X, 'spam'))) # no need for defaults
'''

# 绑定方法事件处理
'''
class HelloClass(object):
    def __init__(self):
        widget=Button(None,text='Hello, event class!',command=self.quit)
        widget.pack()

    def quit(self):
        print('Hello class quit method called')
        sys.exit()

HelloClass()
mainloop()
'''

# 于是我们可以用 self 来保存/传递参数给事件处理器
# 这是GUI编程中一个非常有用的技巧
'''
class SomeGuiClass:
    def __init__(self):
        self.X=42
        self.Y='message'
        Button(text='Hi',command=self.handler)

    def handler(self):
        # 这里可以使用 self.X, self.Y

'''

# Callable对象事件处理器
'''
class HelloCallable:
    def __init__(self):
        self.msg='hello __call__ handler, quit'

    def __call__(self):
        print(self.msg)
        sys.exit()

widget=Button(None,text='Hi event world!',command=HelloCallable())
widget.pack()
widget.mainloop()
'''

# 事件绑定
'''
def hello(event):
    print('Press twice to exit')

def quit(event):
    print('hello, I am going to quit')
    sys.exit()

widget=Button(None,text='Hello event demo')
widget.pack()
# 这里不使用command=handler，用更底层的bind方法绑定事件处理器
widget.bind('<Button-1>',hello)
widget.bind('<Double-1>',quit)
widget.mainloop()
'''

# 添加多个控件
'''
def greeting():
    print('hello, print greeting!')
win=Frame()
win.pack()
Label(win,text='hello, container').pack(side=TOP)
Button(win,text='Greeting',command=greeting).pack(side=LEFT)
Button(win,text='Quit',command=win.quit).pack(side=RIGHT)
win.mainloop()
'''

# 控件大小改变和剪裁
'''
def greeting():
    print('hello, print greeting!')
win=Frame()
win.pack()
Button(win, text='Hello', command=greeting).pack(side=LEFT) 
Button(win, text='Quit', command=win.quit).pack(side=RIGHT) 
Label(win, text='Hello container world').pack(side=TOP)
win.mainloop()
'''

# packer的布局流程 p440
'''
1. 开始时包含整个父容器的可用空间
2. 每个控件放在一边，给它请求整个side的空间，压缩空白部分
3. 后面的控件分配整个剩余部分的空间
4. 最后处理expand和fill参数，扩展和伸缩
'''
# 因此上面的例子调整一下顺序，布局就不同了
def greeting():
    print('hello, print greeting!')
win=Frame()
win.pack()
'''
Button(win, text='Hello', command=greeting).pack(side=LEFT) 
Label(win, text='Hello container world').pack(side=TOP)
Button(win, text='Quit', command=win.quit).pack(side=RIGHT) 
'''
'''
Button(win, text='Hello', command=greeting).pack(side=LEFT,fill=Y)
Label(win, text='Hello container world').pack(side=TOP)
Button(win, text='Quit', command=win.quit).pack(side=RIGHT, expand=YES, fill=X)
'''
'''
win.pack(side=TOP, expand=YES, fill=BOTH)
Button(win, text='Hello', command=greeting).pack(side=LEFT, fill=Y)
Label(win, text='Hello container world').pack(side=TOP)
Button(win, text='Quit', command=win.quit).pack(side=RIGHT, expand=YES,fill=X)
'''
# fill和anchor属性是在根据side属性分配空间之后才应用到控件上
Button(win, text='Hello', command=greeting).pack(side=LEFT, anchor=N) 
Label(win, text='Hello container world').pack(side=TOP)
Button(win, text='Quit', command=win.quit).pack(side=RIGHT)
win.mainloop()


## 自定义控件
# p442











