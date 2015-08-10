#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-09 22:46:54
from __future__ import print_function
import sys
import os
from Tkinter import *
from tkMessageBox import askquestion, askyesno
from tkMessageBox import showerror, showinfo, showwarning

# 高级控件

# Menu 菜单


def notdone():
    showerror('Not implemented', 'Not yet available')
    # print('Not implemented yet.')


def make_win_menu(win):
    # 窗口菜单
    # 将菜单附着到窗口
    top = Menu(win)
    # 连接窗口和菜单
    win.config(menu=top)
    # 将file菜单附着到顶层菜单
    file = Menu(top)
    # underline 指定键盘快捷键
    file.add_command(label='New...', command=notdone, underline=0)
    file.add_command(label='Open...', command=notdone, underline=0)
    file.add_command(label='Quit', command=win.quit, underline=0)
    # 连接父菜单和子菜单
    top.add_cascade(label='File', menu=file, underline=0)

    edit = Menu(top, tearoff=False)
    edit.add_command(label='Cut', command=notdone, underline=0)
    edit.add_command(label='Paste', command=notdone, underline=0)
    # 添加一个分割线，用于分组显示
    edit.add_separator()
    top.add_cascade(label='Edit', menu=edit, underline=0)

    # tearoff 是否显示一个虚线，Mac上无效
    submenu = Menu(edit, tearoff=True)
    submenu.add_command(label='Spam Exit', command=win.quit, underline=0)
    submenu.add_command(label='Eggs None', command=notdone, underline=0)
    edit.add_cascade(label='Stuff', menu=submenu, underline=0)


def win_menu_demo():

    root = Tk()
    root.title('Win Menu')
    make_win_menu(root)
    msg = Label(root, text='window menu basics')
    msg.pack(expand=YES, fill=BOTH)
    msg.config(relief=SUNKEN, width=40, height=7, bg='beige')
    root.mainloop()

# win_menu_demo()


def win_multi_menu_demo():
    root = Tk()
    for i in range(3):
        win = Toplevel(root)
        make_win_menu(win)
        Label(win, bg='black', height=5, width=25).pack(expand=YES, fill=BOTH)
    Button(root, text='Exit', command=root.quit).pack()
    root.mainloop()

# win_multi_menu_demo()


def make_frame_menu(parent):
    # 创建菜单里的Frame容器
    menubar = Frame(parent)
    menubar.pack(side=TOP, fill=X)
    # 将菜单按钮添加到菜单栏
    fbutton = Menubutton(menubar, text='File', underline=0)
    fbutton.pack(side=LEFT)
    # 将菜单添加到菜单按钮
    file = Menu(fbutton)
    file.add_command(label='New...', command=notdone, underline=0)
    file.add_command(label='Open...', command=notdone, underline=0)
    file.add_command(label='Quit', command=parent.quit, underline=0)
    # 连接菜单和菜单按钮
    fbutton.config(menu=file)

    ebutton = Menubutton(menubar, text='Edit', underline=0)
    ebutton.pack(side=LEFT)
    edit = Menu(ebutton, tearoff=False)
    edit.add_command(label='Cut', command=notdone, underline=0)
    edit.add_command(label='Paste', command=notdone, underline=0)
    edit.add_separator()
    ebutton.config(menu=edit)

    submenu = Menu(edit, tearoff=True)
    submenu.add_command(label='Spam Exit', command=parent.quit, underline=0)
    submenu.add_command(label='Eggs None', command=notdone, underline=0)
    edit.add_cascade(label='Stuff', menu=submenu, underline=0)
    return menubar


def frame_menu_demo():
    # 容器/框架菜单，作为普通控件使用
    # 作为普通控件，可嵌入其它容器使用
    root = Tk()
    root.title('Frame Menu')
    make_frame_menu(root)
    Label(root, text='some content', bg='gray', height=5).pack(
        expand=YES, fill=BOTH)
    for i in range(2):
        frm = Frame()
        mu = make_frame_menu(frm)
        mu.config(bd=2, relief=RAISED)
        frm.pack(expand=YES, fill=BOTH)
        msg = Label(root, text='Frame mebu basics')
        msg.pack(expand=YES, fill=BOTH)
        msg.config(relief=SUNKEN, width=40, height=7, bg='beige')
    Button(root, text='Quit', command=root.quit).pack()
    root.mainloop()

# frame_menu_demo()


def menu_button_demo():
    # 事实上，Menubutton可以用在任何地方
    root = Tk()
    root.minsize(320, 240)
    mbutton = Menubutton(root, text='Food')
    picks = Menu(mbutton)
    mbutton.config(menu=picks)
    picks.add_command(label='meat', command=root.quit)
    picks.add_command(label='eggs', command=root.quit)
    picks.add_command(label='fruit', command=root.quit)
    mbutton.pack()
    mbutton.config(bg='white', bd=4, relief=RAISED)
    root.mainloop()

# menu_button_demo()


def option_menu_demo():
    # 下拉选项菜单
    root = Tk()
    var1 = StringVar()
    var2 = StringVar()
    opt1 = OptionMenu(root, var1, 'meat', 'eggs', 'fruit', 'toast')
    opt2 = OptionMenu(root, var2, 'cat', 'dog', 'pig', 'duck')
    opt1.pack(fill=X)
    opt2.pack(fill=X)
    var1.set('eggs')
    var2.set('cat')

    def state():
        print(var1.get(), var2.get())

    Button(root, command=state, text='State').pack()
    root.mainloop()

# option_menu_demo()


class NewMenuDemo(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.createWidgets()
        self.master.title('Toolbars and Menus')
        self.master.iconname('menudemo')

    def createWidgets(self):
        self.makeMenuBar()
        self.makeToolBar()
        l = Label(self, text='Menu and Toolbar Demo')
        l.config(relief=SUNKEN, width=40, height=10, bg='gray')
        l.pack(expand=YES, fill=BOTH)

    def makeToolBar(self, size=(40, 40)):
        # 使用图片按钮
        from PIL.ImageTk import PhotoImage, Image
        imgdir = r'images/'

        toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
        toolbar.pack(side=BOTTOM, fill=X)
        Button(toolbar, text='Hello', command=self.greeting).pack(side=LEFT)
        photos = ('ora-lp4e-big.jpg', 'PythonPoweredAnim.gif',
                  'python_conf_ora.gif')
        self.toolPhotosObjs = []
        for file in photos:
            imgobj = Image.open(imgdir+file)
            imgobj.thumbnail(size, Image.ANTIALIAS)
            img = PhotoImage(imgobj)
            btn = Button(toolbar, image=img, command=self.greeting)
            btn.config(relief=RAISED, bd=2)
            btn.config(width=size[0], height=size[1])
            btn.pack(side=LEFT)
            self.toolPhotosObjs.append((img, imgobj))
        Button(toolbar, text='Quit', command=self.quit).pack(side=RIGHT)

    def makeMenuBar(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.fileMenu()
        self.editMenu()
        self.imageMenu()

    def fileMenu(self):
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Open...', command=self.notdone)
        pulldown.add_command(label='Quit', command=self.quit)
        self.menubar.add_cascade(label='File', underline=0, menu=pulldown)

    def editMenu(self):
        pulldown = Menu(self.menubar)
        pulldown.add_command(label='Paste', command=self.notdone)
        pulldown.add_command(label='Spam', command=self.greeting)
        pulldown.add_separator()
        pulldown.add_command(label='Delete', command=self.greeting)
        pulldown.entryconfig(4, state=DISABLED)
        self.menubar.add_cascade(label='Edit', underline=0, menu=pulldown)

    def imageMenu(self):
        photoFiles = (
            'ora-lp4e.gif', 'pythonPowered.gif', 'python_conf_ora.gif')
        pulldown = Menu(self.menubar)
        self.photoObjs = []
        for file in photoFiles:
            img = PhotoImage(file='gifs/' + file)
            pulldown.add_command(image=img, command=self.notdone)
            self.photoObjs.append(img)  # keep a reference
        self.menubar.add_cascade(label='Image', underline=0, menu=pulldown)

    def greeting(self):
        showinfo('greeting', 'Greetings')

    def notdone(self):
        showerror('Not implemented', 'Not yet available')

    def quit(self):
        if askyesno('Verify quit', 'Are you sure you want to quit?'):
            Frame.quit(self)


# 包含菜单和工具栏的窗口
# NewMenuDemo().mainloop()

class ScrolledList(Frame):
    # 列表框和滚动条 Listboxes and Scrollbars

    def __init__(self, options, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makeWidgets(options)

    def handleList(self, event):
        # 获取当前选中项索引
        index = self.listbox.curselection()
        # 获取索引位置的值
        label = self.listbox.get(index)
        # 也可以用ACTIVE获取当前选中的值
        # label=self.listbox.get(ACTIVE)
        self.runCommand(label)

        # 如果是多选模式的话
        # 默认索引是0开始，0...N-1
        # selections = listbox.curselection()
        # selections = [int(x)+1 for x in selections]

    def makeWidgets(self, options):
        # self.label = Label(self, text='', bg='gray')
        # self.label.pack(side=BOTTOM, fill=X)
        list = Listbox(self, relief=SUNKEN)
        list.config(bg='white', font=('courier', 16))
        # 连接滚动条和列表
        # 只要有yview和xview方法就可以使用滚动条
        # 回调是yscrollcommand和xscrollcommand
        vscroll = Scrollbar(self)
        hscroll = Scrollbar(self, orient='horizontal')
        vscroll.config(command=list.yview, relief=SUNKEN)
        hscroll.config(command=list.xview, relief=SUNKEN)
        list.config(yscrollcommand=vscroll.set)
        list.config(xscrollcommand=hscroll.set)
        # 先添加滚动条，要不然没地方显示
        vscroll.pack(side=RIGHT, fill=Y)
        hscroll.pack(side=BOTTOM, fill=X)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        #pos = 0
        for label in options:
            #list.insert(pos, label)
            #pos += 1
            # 也可以直接使用END
            list.insert(END, label)
        # 列表有四种模式 SINGLE, BROWSE, MULTIPLE, and EXTENDED
        # 默认是BROWSE模式
        # SINGLE 单选模式
        # BROWSE 单选模式，但是允许拖动选中项
        # MULTIPLE 多选模式
        # EXTENDED 多选模式，使用Ctrl/Shift多选
        list.config(selectmode=SINGLE, setgrid=1)
        # 添加事件处理
        list.bind('<Double-1>', self.handleList)
        self.listbox = list

    def runCommand(self, selection):
        # self.label.config(text=selection)
        print('You selected:', selection)


def listbox_scrollbar_demo():
    options = (('No.%s List-Item-Of-Something' % x) for x in range(20))
    ScrolledList(options).mainloop()

#listbox_scrollbar_demo()


# 文本控件 Text
# Text控件是Tk里最强大的控件，支持复杂的字体样式设置，嵌入图片，重做和撤销等
class ScrolledText(Frame):
    def __init__(self,parent=None,text='',file=None):
        Frame.__init__(self,parent)
        self.pack(expand=YES,fill=BOTH)
        self.makeWidgets()
        self.settext(text,file)

    def makeWidgets(self):
        text=Text(self,relief=SUNKEN)
        sbar=Scrollbar(self)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT,fill=Y)
        text.pack(side=LEFT,expand=YES,fill=BOTH)
        self.text=text

    def settext(self,text='',file=None):
        if file:
            text=open(file,'r').read()
        self.text.delete('1.0',END)
        self.text.insert('1.0',text)
        self.text.mark_set(INSERT,'1.0')
        self.text.focus()

    def gettext(self):
        return self.text.get('1.0',END+'-1c')

def scrolled_text_demo():
    root=Tk()
    if len(sys.argv)>1:
        st=ScrolledText(file=sys.argv[1])
    else:
        st=ScrolledText(text='Words\ngo here')

    def show(event):
        print(repr(st.gettext()))

    root.bind('<Key-Escape>',show)
    root.mainloop()

scrolled_text_demo()
# p528 570



































