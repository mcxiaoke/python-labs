#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 13:51:24

from __future__ import print_function
from Tkinter import *

from tkFileDialog import askopenfilename, asksaveasfilename


class ConsoleGuiDemo(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        Label(self, text='Basic Demos').pack()
        Button(self, text='open', command=self.openfile).pack(fill=BOTH)
        Button(self, text='save', command=self.savefile).pack(fill=BOTH)
        self.open_name = self.save_name = ''

    def openfile(self):
        self.open_name = askopenfilename()

    def savefile(self):
        self.save_name = asksaveasfilename(initialdir='~')

if __name__ == '__main__':
    print('popup1...')
    dlg = ConsoleGuiDemo()
    dlg.mainloop()
    print(dlg.open_name)
    print(dlg.save_name)

    print('popup2...')
    dlg = ConsoleGuiDemo()
    dlg.mainloop()
    print(dlg.open_name)
    print(dlg.save_name)
    print('ending...')
