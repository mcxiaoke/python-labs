#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-10 22:33:52


from __future__ import print_function
import sys
import os
from Tkinter import *
from lib import *
from mixin import *
from maker import *

# GuiMixin, GuiMaker demo


class GuiDemo(GuiMixin, GuiMakerWindowMenu):

    def start(self):
        self.hellos = 0
        self.master.title("Gui Demo")
        self.master.iconname('GuiDemo')

        def spawnme():
            self.spawn('demo_mix.py')

        self.menuBar = [
            ('File', 0,
                [
                    ('New...', 0, spawnme),
                    ('Open...', 0, self.fileOpen),
                    ('Quit', 0, self.quit)
                ]
             ),
            ('Edit', 0,
                [('Cut', -1, self.notdone),
                    ('Paste', -1, self.notdone),
                    'separator',
                    ('Stuff', -1,
                     [('Clone', -1, self.clone),
                      ('More', -1, self.more)]
                     ),
                    ('Delete', -1, lambda:0),
                    [5]
                 ]
             ),
            ('Play', 0,
                [('Hello', 0, self.greeting),
                 ('Popups', 0, self.dialog),
                 ('Demos', 0,
                    [('Toplevels', 0, lambda: self.spawn('mixin.py')),
                        ('Frames', 0, lambda: self.spawn('tk2.py')),
                        ('Images', 0, lambda: self.spawn('tk3.py')),
                        ('Counter', 0, lambda:self.spawn('maker.py')),
                        ('Other...', 0, self.pickDemo)]
                  )]
             )]
        self.toolBar = [
            ('Quit', self.quit, dict(side=RIGHT)),
            ('Hello', self.greeting, dict(side=LEFT)),
            ('Popup', self.dialog, dict(side=LEFT, expand=YES))]

    def makeWidgets(self):
        middle = Label(self, text='Hello mixin maker demo',
                       width=40, height=10, relief=SUNKEN,
                       cursor='pencil', bg='white')
        middle.pack(expand=YES, fill=BOTH)

    def greeting(self):
        self.hellos += 1
        if self.hellos % 3:
            print('Hi')
        else:
            self.infobox('Three', 'HELLO!')

    def dialog(self):
        button = self.question('OOPS!', 'You typed rm*... continue?'
                               'questhead', ('yes', 'no'))
        [lambda:None, self.quit][button]()

    def fileOpen(self):
        pick = self.selectOpenFile(file='demo_mixin.py')
        if pick:
            self.browser(pick)

    def more(self):
        new = Toplevel()
        Label(new, text='A new non-modal window').pack()
        Button(new, text='Quit', command=self.quit).pack(side=LEFT)
        Button(new, text='More', command=self.more).pack(side=RIGHT)

    def pickDemo(self):
        pick = self.selectOpenFile(dir='.')
        if pick:
            self.spawn(pick)

if __name__ == '__main__':
    GuiDemo().mainloop()
