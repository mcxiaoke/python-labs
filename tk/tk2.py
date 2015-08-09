#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-09 10:54:20
from __future__ import print_function
import sys
import os
from Tkinter import *

# 基础控件

# 控件列表
'''
Label - 简单的标签
Button - 简单的按钮
Frame - 一个控件容器
Tk - 顶层窗口
Message - 多行标签
Entry - 单行文本域
CheckButton - 多选按钮
RadioButton - 单选按钮
Scale - 缩放滑动杆
PhotoImage - 显示图片的对象
BitmapImage - 显示位图的对象
Menu - 窗口菜单
Menubutton - 打开菜单和子菜单的按钮
Scrollbar - 滚动条
Listbox - 列表选框
Text - 多行文本域，可编辑
Canvas - 画板
'''

# 属性列表
'''
# 几何图形管理器
pack, grid, place
# 绑定变量类型
StringVar, IntVar, DoubleVar, BooleanVar
# 高级控件
SpinBox, LabelFrame, PanedWindow
# 组合控件
Dialog, ScrolledText, OptionMenu
# 延迟回调
after, wait, update
# 其它工具
标准对话框，剪贴板，绑定和事件，控件属性，定制和模态对话框，动画技术
# 扩展
Tix, ttk, Pmw
'''

# Tk和Tinter的语法对应关系
'''
Tcl                             Tinter
Frame .panel                    panel=Frame()
button .panel.quit              quit=Button(panel)
button .panel.go -fg black      go=Button(panel.fg='black')
.panel.go -bg red               go.config(bg='red') go['bg']='red'
.popup invoke                   popup.invoke()
pack .panel -side left -fill x   panel.pack(side=LEFT,fill=X)
'''

# 修改样式
# config方法可以在任何时候调用


def configure_label():
    root = Tk()
    # 字形的取值 normal, bold, roman, italic, underline, over strike
    # 这三种字体在所有平台可用：Times/Courier/Helvetica
    labelfont = ('times', 20, 'bold')
    widget = Label(root, text='hello configure button')
    # 背景色，前景色
    # 颜色可以使用名字或者 #ffff00 这种形式
    widget.config(bg='black', fg='yellow')
    # 字体样式
    widget.config(font=labelfont)
    # 宽度和高度
    widget.config(height=3, width=20)
    # 扩展和填充
    widget.pack(expand=YES, fill=BOTH)
    root.mainloop()

# configure_label()

# 其它可用属性
'''
bd - border的取值 FLAT, SUNKEN, RAISED, GROOVE, SOLID, or RIDGE
cursor - 更改光标的样式，取值 gumby, watch, pencil, cross, and hand2
state - 状态，取值 DISABLED, NORMAL, READONLY等
padding - 边距，padx, pady

'''


def configure_button():
    widget = Button(text='Hello Button', padx=10, pady=10)
    widget.pack(padx=20, pady=20)
    widget.config(cursor='gumby')
    widget.config(bd=8, relief=RAISED)
    # 这句好像无效，Mac上
    widget.config(bg='dark green', fg='white')
    widget.config(font=('helvetica', 20, 'underline italic'))
    widget.mainloop()

# configure_button()

# 顶层窗口
'''
Tkinter有一个应用顶层窗口，还可以创建任意数量的独立窗口或弹出窗口
使用Tk()和Toplevel()创建，共享一个消息循环，在同一个进程
每个窗口可以独立放大，缩小和关闭
但是，点击默认主窗口的关闭会关闭整个应用
'''


def create_toplevel():
    # 默认会创建一个顶层窗口
    # 这里win1和win2是另外两个窗口
    win1 = Toplevel()
    win2 = Toplevel()
    Button(win1, text='Button1', command=sys.exit).pack()
    Button(win2, text='Button2', command=sys.exit).pack()
    # 这个位于默认的Tk()窗口
    Label(text='Popups').pack()
    win1.mainloop()

# create_toplevel()

# 顶层窗口和Tk控件
'''
Toplevel类似于Frame，但是它有自己的窗口和额外的方法，有顶层窗口的一些属性
Tk也是一个Toplevel，它是应用的根窗口 root window，它没有父窗口

这个
Label(text='Popups').pack()
等价于
root=Tk()
Label(root,text='Popups).pack()
root.mainloop()
'''

# 可以不显示默认的Root窗口
''


def no_default_root():
    Tkinter.NoDefaultRoot()
    win1 = Tk()
    win2 = Tk()
    # win1.destroy只关闭当前窗口，sys.exit会结束整个进程
    Button(win1, text='Button1', command=win1.destroy).pack()
    Button(win2, text='Button2', command=win2.destroy).pack()
    win1.mainloop()

# no_default_root()

# 顶层窗口的接口


def top_window_protocols():
    root = Tk()
    trees = [('Breakfirst!', 'light blue'),
             ('Launch!', 'dark green'),
             ('Eat meat', 'red')]

    for(tree, color) in trees:
        win = Toplevel(root)
        # title 指定窗口的标题
        win.title('A Window')
        # protocol指定点击关闭按钮的行为，WM_DELETE_WINDOW是关闭窗口
        win.protocol('WM_DELETE_WINDOW', lambda: None)
        # iconbitmap 设置窗口的图标
        win.iconbitmap('py-blue-trans-out.ico')
        # 设置窗口最小大小
        win.minsize(320, 240)
        # 设置窗口最大的大小
        win.maxsize(800, 600)
        # destroy 表示关闭某个窗口和它的子窗口
        # quit 表示关闭所有窗口
        msg = Button(win, text=tree, command=win.destroy)
        msg.pack(expand=YES, fill=BOTH)
        msg.config(padx=10, pady=10, bd=10, relief=RAISED)
        # Button的颜色设置在Mac上无效，原因未知
        msg.config(bg='black', fg=color, font=('times', 30, 'bold italic'))

    root.title('Root Window')
    Label(root, text='Main Window', width=30).pack()
    Button(root, text='Quit App', command=root.quit).pack()
    root.mainloop()


# top_window_protocols()


# 事件绑定

def binding_events():
    def showPostEvent(event):
        print('Widget=%s X=%s Y=%s' % (event.widget, event.x, event.y))

    def showAllEvent(event):
        print(event)
        for attr in dir(event):
            if not attr.startswith('__'):
                print(attr, '=>', getattr(event, attr))

    def onKeyPress(event):
        print('Got key press:', event.char)

    def onArrowKey(event):
        print('Got up arrow key press')

    def onReturnKey(event):
        print('Got return key press')

    def onLeftClick(event):
        print('Got left mouse button click:', end=' ')
        showPostEvent(event)

    def onRightClick(event):
        print('Got right mouse button click:', end=' ')
        showPostEvent(event)

    def onMiddleClick(event):
        print('Got middle mouse button click:', end=' ')
        showPostEvent(event)
        showAllEvent(event)

    def onLeftDrag(event):
        print('Got left mouse button drag:', end=' ')
        showPostEvent(event)

    def onDoubleLeftClick(event):
        print('Got double left mouse click', end=' ')
        showPostEvent(event)
        tkroot.quit()

    tkroot = Tk()
    labelfont = ('courier', 20, 'bold')
    widget = Label(tkroot, text='Hello bind event')
    widget.config(bg='red', font=labelfont)
    widget.config(height=5, width=20)
    widget.pack(expand=YES, fill=BOTH)

    widget.bind('<Button-1>', onLeftClick)  # 鼠标左键
    widget.bind('<Button-2>', onRightClick)  # 鼠标右键
    widget.bind('<Button-3>', onMiddleClick)  # 鼠标滚轮
    widget.bind('<Double-1>', onDoubleLeftClick)  # 鼠标左键双击
    widget.bind('<B1-Motion>', onLeftDrag)  # 鼠标左键拖拽

    widget.bind('<KeyPress>', onKeyPress)  # 键盘按键
    widget.bind('<Up>', onArrowKey)  # 键盘方向键
    # widget.bind('<Down>', onArrowKey) # 键盘方向键
    # widget.bind('<Left>', onArrowKey) # 键盘方向键
    # widget.bind('<Right>', onArrowKey) # 键盘方向键
    widget.bind('<Return>', onReturnKey)  # 键盘回车键
    widget.focus()
    tkroot.title('Click Me')
    tkroot.mainloop()

    # 其它的事件绑定
    '''
    <ButtonPress> 按钮按下
    <ButtonRelease> 按钮释放
    <Motion> 鼠标移动
    <Enter>和<Leave> 鼠标指针进入和离开某个区域
    <Configure> 窗口大小和位置改变等
    <Destroy> 窗口销毁时
    <FocusIn>和<Focusout> 控件获得和失去焦点时
    <Map>和<Unmap> 窗口打开和最小化时
    <Escape>/<Backspace>/<Tab> 特殊按键事件
    <Up>/<Down>/<Left>/<Right> 方向按键
    <B1-Motion> 表示鼠标左键按下并移动
    <KeyPress-a> 表示按下键盘上的a
    '''

# binding_events()


# Message和Entry

# Message控件用于显示简单的文本

def simple_message():
    msg = Message(
        text='Oh, by the way, this is just a simple message text, hahahah !')
    msg.config(bg='pink', font=('times', 16, 'italic'))
    msg.pack(fill=X, expand=YES)
    mainloop()

# simple_message()

# Entry控件单行文本框
# 支持滚动，支持编辑和选择事件绑定


def simple_entry():
    from tk2_quitter import Quitter

    def fetch():
        print('Input => "%s"' % ent.get())
        # ent.config(state=DISABLED)

    root = Tk()
    ent = Entry(root)
    ent.delete(0, END)
    ent.insert(0, 'Type words here')
    ent.pack(side=TOP, fill=X)

    ent.focus()
    ent.bind('<Return>', (lambda event: fetch()))  # 绑定回车键事件
    btn = Button(root, text='Fetch', command=fetch)
    btn.pack(side=LEFT)
    Quitter(root).pack(side=RIGHT)
    root.mainloop()


# simple_entry()

# 表单布局示例
def entry_form_layout():
    from tk2_quitter import Quitter
    fields = 'Name', 'Job', 'Pay'

    def fetch(entries):
        for entry in entries:
            print('Input => "%s"' % entry.get())

    def makeform(root, fields):
        entries = []
        for field in fields:
            row = Frame(root)
            lab = Label(row, width=5, text=field)
            ent = Entry(row)
            row.pack(side=TOP, fill=X)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append(ent)
        return entries

    def show(entries, popup):
        # 必须在弹出窗口销毁之前收集数据
        fetch(entries)
        popup.destroy()

    # 显示模态输入表单
    def ask():
        popup = Toplevel()
        ents = makeform(popup, fields)
        Button(popup, text='OK', command=(lambda: show(ents, popup))).pack()
        popup.grab_set()
        popup.focus_get()
        popup.wait_window()

    root = Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event: fetch(ents)))
    Button(root, text='Fetch', command=(lambda: fetch(ents))).pack(side=LEFT)
    Button(root, text='Popup', command=ask).pack(side=RIGHT)
    Quitter(root).pack(side=RIGHT)
    root.mainloop()

# entry_form_layout()

# 可变属性和表单布局
# StringVar, IntVar, DoubleVar, and Boolean Var


def variables_form_layout():
    from tk2_quitter import Quitter
    fields = 'Name', 'Job', 'Pay', 'Value', 'Address'

    def fetch(variables):
        for variable in variables:
            print('Input => "%s"' % variable.get())

    def makeform(root, fields):
        form = Frame(root)
        left = Frame(form)
        right = Frame(form)
        form.pack(fill=X)
        left.pack(side=LEFT)
        right.pack(side=RIGHT, expand=YES, fill=X)

        variables = []
        for field in fields:
            # Label和Entry没有关联起来，所以它们可能没对齐
            lab = Label(left, width=8, text=field)
            ent = Entry(right)
            lab.pack(side=TOP)
            ent.pack(side=TOP, fill=X)
            var = StringVar()
            ent.config(textvariable=var)
            var.set('enter here')
            variables.append(var)
        return variables

    def show(variables, popup):
        popup.destroy()
        # 使用StringVar，在窗口销毁之后也可以获取数据
        fetch(variables)

    # 显示模态输入表单
    def ask():
        popup = Toplevel()
        vars = makeform(popup, fields)
        Button(popup, text='OK', command=(lambda: show(vars, popup))).pack()
        popup.grab_set()
        popup.focus_get()
        popup.wait_window()

    root = Tk()
    vars = makeform(root, fields)
    Button(root, text='Fetch', command=(lambda: fetch(vars))).pack(side=LEFT)
    Button(root, text='Popup', command=ask).pack(side=RIGHT)
    Quitter(root).pack(side=RIGHT)
    root.bind('<Return>', (lambda event: fetch(vars)))
    root.mainloop()


# variables_form_layout()

# 单选和多选按钮
# CheckButton, RadioButton, Scale

from tk2_dialog_table import demos
from tk2_quitter import Quitter


class CheckDemo(Frame):

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack()
        self.tools()
        Label(self, text='Check Demos').pack()
        self.vars = []
        for key in demos:
            var = IntVar()
            Checkbutton(self, text=key,
                        variable=var, command=demos[key]).pack(side=LEFT)
            self.vars.append(var)

    def report(self):
        for var in self.vars:
            # 勾选的返回1，没勾选的默认0
            print(var.get(), end=' ')
        print()

    def tools(self):
        frm = Frame(self)
        frm.pack(side=RIGHT)
        Button(frm, text='State', command=self.report).pack(fill=X)
        Quitter(frm).pack(fill=X)

# CheckDemo().mainloop()


def manual_check_demo():
    # 自己保存状态的复选按钮
    states = []

    def onPress(i):
        states[i] = not states[i]

    root = Tk()
    for i in range(10):
        chk = Checkbutton(root, text=str(i), command=(lambda i=i: onPress(i)))
        chk.pack(side=LEFT)
        states.append(False)

    root.mainloop()
    print(states)

# manual_check_demo()


def auto_check_demo():
    root = Tk()
    states = []
    for i in range(10):
        var = IntVar()
        chk = Checkbutton(root, text=str(i), variable=var)
        chk.pack(side=LEFT)
        states.append(var)
    root.mainloop()
    print([v.get() for v in states])
# auto_check_demo()

from tk2_dialog_table import demos
from tk2_quitter import Quitter


class RadioDemo(Frame):

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack()
        Label(self, text='Radio Demos').pack(side=TOP)
        self.var = StringVar()
        # 为了确保是单选，需要给每个Radiobutton分配统一的variable，不同的value
        for key in demos:
            Radiobutton(self, text=key, command=self.onPress,
                        variable=self.var, value=key).pack(anchor=NW)
        self.var.set(key)
        Button(self, text='State', command=self.report).pack(fill=X)
        Quitter(self).pack(fill=X)

    def onPress(self):
        pick = self.var.get()
        print('you pressed', pick)
        print('result:', demos[pick]())

    def report(self):
        print(self.var.get())


# RadioDemo().mainloop()


def manual_radio_demo():
    state = ''
    buttons = []

    def onPress(i):
        global state
        state = i
        for btn in buttons:
            btn.deselect()
        buttons[i].select()

    root = Tk()
    for i in range(10):
        rad = Radiobutton(root, text=str(i),
                          value=str(i), command=(lambda i=i: onPress(i)))
        rad.pack(side=LEFT)
        buttons.append(rad)

    onPress(0)
    root.mainloop()
    print(state)

# manual_radio_demo()


def auto_radio_demo():
    root = Tk()
    var = IntVar(0)
    for i in range(10):
        rad = Radiobutton(root, text=str(i), value=i, variable=var)
        rad.pack(side=LEFT)
    root.mainloop()
    print(var.get())

# auto_radio_demo()


def clear_radio_demo():
    root = Tk()
    tmp = IntVar()

    def radio():
        # 临时变量，会自动析构，需要保存在外部
        # 导致的结果是点击无效，没有项会被选中
        # tmp=IntVar()
        for i in range(10):
            rad = Radiobutton(root, text=str(i), value=i, variable=tmp)
            rad.pack(side=LEFT)
        tmp.set(5)
    radio()
    root.mainloop()
    print(tmp.get())

# clear_radio_demo()

# 滑杆控件 Scale Slider
# 通过共享 IntVar变量，可以让多个控件的值和界面同步

from tk2_dialog_table import demos
from tk2_quitter import Quitter


class ScaleDemo(Frame):

    '''
    Scale控件属性：
    label - 放置在滑杆边的说明文本
    length - 指定滑杆的长度
    orient - 指定滑杆的方向
    from_/to - 指定最小值和最大值
    tickinterval - 指定显示的值的间隔
    resolution - 指定拖动滑杆时的跳动单位
    showvalue - 显示滑杆的当前值

    '''

    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack()
        Label(self, text='Scale Demos').pack()
        self.var = IntVar()
        Scale(self, label='Pick demo number A',
              command=self.onMove, variable=self.var,
              from_=0, to=len(demos)-1).pack()
        Scale(self, label='Pick demo number B',
              command=self.onMove, variable=self.var,
              from_=0, to=len(demos)-1,
              length=200, tickinterval=1,
              showvalue=YES, orient='horizontal').pack()
        Quitter(self).pack(side=RIGHT)
        Button(self, text='Run demo', command=self.onRun).pack(side=LEFT)
        Button(self, text='State', command=self.report).pack(side=RIGHT)

    def onMove(self, value):
        print('in Move', value)

    def onRun(self):
        pos = self.var.get()
        print('you picked', pos)
        demo = list(demos.values())[pos]
        print(demo())

    def report(self):
        print(self.var.get())

# print(list(demos.keys()))
# ScaleDemo().mainloop()


def scale_simple_demo():
    root = Tk()
    # 共享变量同步状态
    var = IntVar(0)
    scl1 = Scale(root, from_=-100, to=100, tickinterval=50, resolution=10)
    scl1.config(variable=var)
    scl1.pack(side=LEFT, expand=YES, fill=Y)
    scl2 = Scale(root, from_=-100, to=100, tickinterval=50, resolution=10)
    scl2.config(variable=var)
    scl2.pack(side=RIGHT, expand=YES, fill=Y)

    def report():
        print(scl1.get(), scl2.get())
    Button(root, text='State', command=report).pack(side=RIGHT)
    root.mainloop()

# scale_simple_demo()

# 运行控件的三种方式
# 1. 嵌入其它的容器类控件
# 2. 运行在自己的顶层窗口
# 3. 启动为单独的程序

# 创建可复用的组件库


class Checkbar(Frame):

    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return [var.get() for var in self.vars]


class Radiobar(Frame):

    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.var = StringVar()
        self.var.set(picks[0])
        for pick in picks:
            rad = Radiobutton(
                self, text=pick, value=pick, variable=self.var)
            rad.pack(side=side, anchor=anchor, expand=YES)

    def state(self):
        return self.var.get()


def button_bars_demo():
    root = Tk()
    lng = Checkbar(root, ['Python', 'C#', 'Java', 'C++'])
    gui = Radiobar(root, ['win', 'x11', 'mac'], side=TOP, anchor=NW)
    tgl = Checkbar(root, ['All'])

    gui.pack(side=LEFT, fill=Y)
    lng.pack(side=TOP, fill=X)
    tgl.pack(side=LEFT)

    lng.config(relief=GROOVE, bd=2)
    gui.config(relief=RIDGE, bd=2)

    def allstates():
        print(gui.state(), lng.state(), tgl.state())

    from tk2_quitter import Quitter
    Quitter(root).pack(side=RIGHT)
    Button(root, text='Peek', command=allstates).pack(side=RIGHT)
    root.mainloop()

# button_bars_demo()

# 显示图片
# 默认只支持GIF,PPM,PGM格式
# 其它格式可通过PIL支持
# 需要持有图片的引用，如果图片被回收，显示界面也会丢失
gifdir = '../../gifs/'
from glob import glob
import random


def image_button_simple():
    win = Tk()
    img = PhotoImage(file=gifdif+'ora-pp.gif')
    Button(win, image=img).pack()
    win.mainloop()

# image_button_simple()


def image_canvas_simple():
    win = Tk()
    img = PhotoImage(file=gifdir+'ora-lp4e.gif')
    can = Canvas(win)
    can.pack(fill=BOTH)
    can.config(width=img.width(), height=img.height())
    can.create_image(2, 2, image=img, anchor=NW)
    win.mainloop()

# image_canvas_simple()


def button_pictures_fun():

    def draw():
        name, photo = random.choice(images)
        lbl.config(text=name)
        pix.config(image=photo)

    root = Tk()
    lbl = Label(root, text='None', bg='blue', fg='red')
    pix = Button(root, text='Press me', command=draw, bg='white')
    lbl.pack(fill=BOTH)
    pix.pack(pady=10)
    CheckDemo(root, relief=SUNKEN, bd=2).pack(fill=BOTH)
    files = glob(gifdif+"*.gif")
    images = [(x, PhotoImage(file=x)) for x in files]
    print(files)
    root.mainloop()

# button_pictures_fun()


class ButtonPicsDemo(Frame):

    def __init__(self, gifdir=gifdir, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.lbl = Label(self, text='None', bg='blue', fg='red')
        self.pix = Button(self, text='press me', command=self.draw, bg='white')
        self.lbl.pack(fill=BOTH)
        self.pix.pack(pady=10)
        CheckDemo(self, relief=SUNKEN, bd=2).pack(fill=BOTH)
        files = glob(gifdir+"*.gif")
        self.images = [(x, PhotoImage(file=x)) for x in files]
        print(files)

    def draw(self):
        name, photo = random.choice(self.images)
        self.lbl.config(text=name)
        self.pix.config(image=photo)


# ButtonPicsDemo().mainloop()

# PIL图像处理和显示
# PIL支持30多种格式，如GIF,JPEG,TIFF,PNG,BMP
'''
from PIL import ImageTk
photoimg = ImageTk.PhotoImage(file=imgdir + "spam.jpg") 
Button(image=photoimg).pack()

from PIL import Image, ImageTk
imageobj = Image.open(imgdir + "spam.jpeg") 
photoimg = ImageTk.PhotoImage(imageobj) 
Button(image=photoimg).pack()
'''


def pil_image_viewer():
    from PIL.ImageTk import PhotoImage
    imgdir = 'images'
    imgfile = 'florida-2009-1.jpg'
    if len(sys.argv) > 1:
        imgfile = sys.argv[1]
    imgpath = os.path.join(imgdir, imgfile)

    win = Tk()
    win.title(imgfile)
    imgobj = PhotoImage(file=imgpath)
    Label(win, image=imgobj).pack()
    win.mainloop()
    print(imgobj.width(), imgobj.height())

# pil_image_viewer()


def pil_image_dir():
    from PIL.ImageTk import PhotoImage
    imgdir = 'images'
    if len(sys.argv) > 1:
        imgdir = sys.argv[1]
    imgfiles = os.listdir(imgdir)

    main = Tk()
    main.title('Image Viewer')
    quit = Button(
        main, text='Quit all', command=main.quit, font=('courier', 25))
    quit.pack()
    savephotos = []

    for imgfile in imgfiles:
        imgpath = os.path.join(imgdir, imgfile)
        win = Toplevel()
        win.title(imgfile)
        try:
            imgobj = PhotoImage(file=imgpath)
            Label(win, image=imgobj).pack()
            print(imgpath, imgobj.width(), imgobj.height())
            savephotos.append(imgobj)
        except Exception:
            errmsg = 'skipping %s\n%s' % (imgfile, sys.exc_info()[1])
            Label(win, text=errmsg).pack()
        main.mainloop()

# pil_image_dir().mainloop()


def grid_layout_demo():

    def report(name):
        print('pressed button: %s' % name)

    win = Tk()
    win.title('Grid Demo')
    for i in range(10):
        for j in range(5):
            btn = Button(win, text='Button %d-%d' % (i, j),
                         command=(lambda i=i, j=j: report("%d-%d" % (i, j))))
            btn.grid(row=i, column=j)

    Button(win, text='Quit', command=win.quit).grid(columnspan=5, stick=EW)
    win.mainloop()

grid_layout_demo()
