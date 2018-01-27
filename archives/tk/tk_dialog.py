#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-09 18:23:55


# 标准对话框

from Tkinter import *
from tkMessageBox import *

def simple_dialog():
    # from tkinter.messagebox import *
    def callback():
        # 确认对话框
        if askyesno('Verify', 'Do you really want to quit?'):
            # 警告对话框
            showwarning('Yes', 'Quit not ye implemented')
        else:
            # 信息提示对话框
            showinfo('No', 'Quit has been cancelled')
    errmsg = 'Sorry, no Spam allowed'
    Button(text='Quit', command=callback).pack(fill=X)
    Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(
        fill=X)
    mainloop()

# simple_dialog()

# 可复用的退出按钮


def quit_button():
    from tkMessageBox import askokcancel

    class Quitter(Frame):

        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack()
            widget = Button(self, text='Quit', command=self.quit)
            widget.pack(side=LEFT, expand=YES, fill=BOTH)

        def quit(self):
            ans = askokcancel('Verify exit', 'Really quit?')
            if ans:
                Frame.quit(self)

    Quitter().mainloop()

# quit_button()

#  对话框启动器示例


def dialog_demos():
    from tk2_dialog_table import demos
    from tk2_quitter import Quitter

    class Demo(Frame):

        def __init__(self, parent=None, **options):
            Frame.__init__(self, parent, **options)
            self.pack()
            Label(self, text='Basic Demos').pack()
            for (key, value) in demos.items():
                # Button(self,text=key,command=value).pack(side=TOP,fill=BOTH)
                func = (lambda key=key: self.printit(key))
                Button(self, text=key, command=func).pack(side=TOP, fill=BOTH)
            Quitter(self).pack(side=TOP, fill=BOTH)

        def printit(self, name):
            print(name, 'return=>', demos[name]())

    Demo().mainloop()

# dialog_demos()

# 设置颜色


def set_color_demo():
    from tkColorChooser import askcolor

    def setBgColor():
        (triple, hexstr) = askcolor()
        if hexstr:
            print('color you selected:', hexstr)
            root.config(bg=hexstr)
    root = Tk()
    root.minsize(320, 240)
    push = Button(root, text='Set background color', command=setBgColor)
    push.config(font=('times', 20, 'bold'))
    push.pack(expand=YES)
    root.mainloop()


# set_color_demo()

# 自定义对话框

def create_custom_dialog():
    modal = True if sys.argv and len(sys.argv) > 1 else False

    def dialog():
        print('modal is ', modal)
        win = Toplevel()
        Label(win, text='Hard drive reformatted!').pack()
        Button(win, text='OK', command=win.destroy).pack()
        if modal:
            win.focus_get()
            win.grab_set()
            win.wait_window()
        print('dialog exit')
    root = Tk()
    root.minsize(320, 240)
    Button(root, text='popup', command=dialog).pack()
    root.mainloop()

# create_custom_dialog()

# 递归对话框


def create_recursive_dialog():
    def dialog():
        win = Toplevel()
        Label(win, text='Hard drive reformatted!').pack()
        Button(win, text='OK', command=win.quit).pack()
        win.protocol('WM_DELETE_WINDOW', win.quit)
        win.focus_get()
        win.grab_set()
        # 这里调用了mainloop()
        # 必须调用quit才能终止
        # 调用destroy没有效果
        # mainloop()+quit效果和wait_window差不多
        win.mainloop()
        win.destroy()
        print('dialog exit')
    root = Tk()
    Button(root, text='Popup', command=dialog).pack()
    root.mainloop()

create_recursive_dialog()
