#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-10 21:24:18

# GUI编码技术

from __future__ import print_function
import sys
import os
from Tkinter import *
from lib import *
from tkSimpleDialog import *
from tkFileDialog import *
from tkMessageBox import *
from launchmodes import PortableLauncher,System

class GuiMixin:

    def infobox(self,title,text,*args):
        return showinfo(title,text)

    def errorbox(self,text):
        showerror('Error!',text)

    def question(self,title,text,*args):
        return askyesno(title,text)

    def notdone(self):
        showerror('Not implemented','Option not available')

    def quit(self):
        ans=self.question('Verify quit','Are you sure you want to quit?')
        if ans:
            Frame.quit(self)

    def help(self):
        self.infobox('RTFM','See figure 1...')

    def selectOpenFile(self,file='',dir=''):
        return askopenfilename(initialdir=dir,initialfile=file)

    def selectSaveFile(self,file='',dir=''):
        return asksaveasfilename(initialfile=file,initialdir=dir)

    def clone(self,args=()):
        new=Toplevel()
        myclass=self.__class__
        myclass(new,*args)

    def spawn(self,pycmdline,  wait=False):
        if not wait:
            PortableLauncher(pycmdline,pycmdline)()
        else:
            System(pycmdline,pycmdline)()

    def browser(self,filename):
        new=Toplevel()
        view=ScrolledText(new,file=filename)
        view.text.config(height=30,width=85)
        view.text.config(font=('courier',12,'normal'))
        new.title('Text Viewer')
        new.iconname('brower')


def _mixin_demo():
    class TestMixin(GuiMixin,Frame):
        def __init__(self,parent=None):
            Frame.__init__(self,parent)
            self.pack()
            Button(self,text='quit',command=self.quit).pack(fill=X)
            Button(self,text='help',command=self.help).pack(fill=X)
            Button(self,text='clone',command=self.clone).pack(fill=X)
            Button(self,text='spawn',command=self.other).pack(fill=X)

        def other(self):
            self.spawn('mixin.py')

    TestMixin().mainloop()

if __name__ == '__main__':
    _mixin_demo()
