#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-10 22:07:17

from __future__ import print_function
import sys
import os
from Tkinter import *
from tkMessageBox import *

# make menus


class GuiMaker(Frame):
    menuBar = []
    toolBar = []
    helpButton = True

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.start()
        self.makeMenuBar()
        self.makeToolBar()
        self.makeWidgets()

    def makeMenuBar(self):
        """
        make menu bar at the top (Tk8.0 menus below)
        expand=no, fill=x so same width on resize
        """
        menubar = Frame(self, relief=RAISED, bd=2)
        menubar.pack(side=TOP, fill=X)

        for (name, key, items) in self.menuBar:
            mbutton  = Menubutton(menubar, text=name, underline=key)
            mbutton.pack(side=LEFT)
            pulldown = Menu(mbutton)
            self.addMenuItems(pulldown, items)
            mbutton.config(menu=pulldown)

        if self.helpButton:
            Button(menubar, text    = 'Help',
                            cursor  = 'gumby',
                            relief  = FLAT,
                            command = self.help).pack(side=RIGHT)

    def addMenuItems(self, menu, items):
        for item in items:                     # scan nested items list
            if item == 'separator':            # string: add separator
                menu.add_separator({})
            elif type(item) == list:           # list: disabled item list
                for num in item:
                    menu.entryconfig(num, state=DISABLED)
            elif type(item[2]) != list:
                menu.add_command(label     = item[0],         # command:
                                 underline = item[1],         # add command
                                 command   = item[2])         # cmd=callable
            else:
                pullover = Menu(menu)
                self.addMenuItems(pullover, item[2])          # sublist:
                menu.add_cascade(label     = item[0],         # make submenu
                                 underline = item[1],         # add cascade
                                 menu      = pullover)

    def makeToolBar(self):
        '''
        make button bar at bottom
        expand=no, fill=x,
        '''
        if self.toolBar:
            toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
            toolbar.pack(side=BOTTOM, fill=X)
            for (name, action, where) in self.toolBar:
                Button(toolbar, text=name, command=action).pack(where)

    def makeWidgets(self):
        name = Label(self, width=40, heigh=10,
                     relief=SUNKEN, bg='white',
                     text=self.__class__.__name__,
                     cursor='crosshair')
        name.pack(expand=YES, fill=BOTH, side=TOP)

    def help(self):
        showinfo('Help', 'Sorry, no help for ' + self.__class__.__name__)

    def start(self):
        # subclass override this method
        pass

GuiMakeFrameMenu = GuiMaker


class GuiMakerWindowMenu(GuiMaker):

    def makeMenuBar(self):
        menubar = Menu(self.main)
        self.main.config(menu=menubar)

        for (name, key, items) in self.menuBar:
            pulldown = Menu(menubar)
            self.addMenuItems(pulldown, items)
            menubar.add_cascade(label=name, underline=key, menu=pulldown)

        if self.helpButton:
            if sys.platform[:3] == 'win':
                menubar.add_command(label='Help', command=self.help)
            else:
                pulldown = Menu(menubar)
                pulldown.add_command(label='About', command=self.help)
                menubar.add_cascade(label='Help', menu=pulldown)


def menu_maker_test():
    from mixin import GuiMixin
    menuBar = [
        ('File', 0,
            [('Open', 0, lambda:0),
             ('Quit', 0,
                [('Sub 1', 0, sys.exit),
                    ('Sub 2', 0, lambda:0)
                 ])]),
        ('Edit', 0,
            [('Cut', 0, lambda:0),
             ('Paste', 0, lambda:0)])]

    toolBar = [('Quit', sys.exit, {'side': LEFT})]

    class TestAppFrameMenu(GuiMixin, GuiMakeFrameMenu):

        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar

    class TestAppWindowMenu(GuiMixin, GuiMakerWindowMenu):

        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar

    class TestAppWindowMenuBasic(GuiMakerWindowMenu):

        def start(self):
            self.menuBar = menuBar
            self.toolBar = toolBar

    root = Tk()
    TestAppFrameMenu(Toplevel())
    TestAppWindowMenu(Toplevel())
    TestAppWindowMenuBasic(root)
    root.mainloop()

if __name__ == '__main__':
    menu_maker_test()
