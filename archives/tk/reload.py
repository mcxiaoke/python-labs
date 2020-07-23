#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 10:40:07
from __future__ import print_function
from Tkinter import *
import mmodule
from imp import reload

# 模块动态加载示例

class Hello(Frame):
    def __init__(self,main=None):
        Frame.__init__(self,main)
        self.pack()
        self.makeWidgets()

    def makeWidgets(self):
        Button(self,text='Message1',command=self.message1).pack(side=LEFT)
        Button(self,text='Message2',command=self.message2).pack(side=RIGHT)

    def message1(self):
        reload(mmodule)
        mmodule.message1()

    def message2(self):
        reload(mmodule)
        mmodule.message2(self)

    def method1(self):
        print('exposed method...')

Hello().mainloop()

