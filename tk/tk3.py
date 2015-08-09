#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-09 22:46:54
from __future__ import print_function
import sys
import os
from Tkinter import *
from tkMessageBox import askquestion, showerror

# 高级控件

# Menu 菜单
def notdone():
    showerror('Not implemented','Not yet available')
    # print('Not implemented yet.')

def makemenu(win):
    # 窗口菜单
    # 将菜单附着到窗口
    top=Menu(win)
    # 连接窗口和菜单
    win.config(menu=top)
    # 将file菜单附着到顶层菜单
    file=Menu(top)
    # underline 指定键盘快捷键
    file.add_command(label='New...',command=notdone,underline=0)
    file.add_command(label='Open...',command=notdone,underline=0)
    file.add_command(label='Quit',command=win.quit,underline=0)
    # 连接父菜单和子菜单
    top.add_cascade(label='File',menu=file,underline=0)

    edit=Menu(top,tearoff=False)
    edit.add_command(label='Cut',command=notdone,underline=0)
    edit.add_command(label='Paste',command=notdone,underline=0)
    # 添加一个分割线，用于分组显示
    edit.add_separator()
    top.add_cascade(label='Edit',menu=edit,underline=0)

    # tearoff 是否显示一个虚线，Mac上无效
    submenu=Menu(edit,tearoff=True)
    submenu.add_command(label='Spam Exit',command=win.quit,underline=0)
    submenu.add_command(label='Eggs None',command=notdone,underline=0)
    edit.add_cascade(label='Stuff',menu=submenu,underline=0)

def win_menu_demo():

    root=Tk()
    root.title('Win Menu')
    makemenu(root)
    msg=Label(root,text='window menu basics')
    msg.pack(expand=YES, fill=BOTH)
    msg.config(relief=SUNKEN, width=40,height=7,bg='beige')
    root.mainloop()

#win_menu_demo()

def win_multi_menu_demo():
    root=Tk()
    for i in range(3):
        win=Toplevel(root)
        makemenu(win)
        Label(win,bg='black',height=5,width=25).pack(expand=YES,fill=BOTH)
    Button(root,text='Exit',command=root.quit).pack()
    root.mainloop()

#win_multi_menu_demo()

def frame_menu_demo():
    # 容器/框架菜单
    # p512,544


















