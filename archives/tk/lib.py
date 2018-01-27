#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-10 21:25:48
from __future__ import print_function
import sys
import os
from Tkinter import *


class ScrolledText(Frame):

    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        # 自动扩展空间
        self.pack(expand=YES, fill=BOTH)
        self.makeWidgets()
        self.settext(text, file)

    def makeWidgets(self):
        text = Text(self, relief=SUNKEN)
        sbar = Scrollbar(self)
        # 连接滚动条
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        # 先布置滚动条
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text

    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        # 删除当前的文本
        self.text.delete('1.0', END)
        # 从最开始插入新文本
        self.text.insert('1.0', text)
        # 光标移动到开头
        self.text.mark_set(INSERT, '1.0')
        # 获取焦点
        self.text.focus()

    def insert(self, index, text=''):
        self.text.insert(index, text)

    def see(self, index):
        self.text.see(index)

    def bind(self, sequence, func):
        self.text.bind(sequence, func)

    def update(self):
        self.text.update()

    def gettext(self):
        # 返回全部文本
        # 1.0 表示第1行第0列 -1c表示一个字符之前
        return self.text.get('1.0', END+'-1c')
