#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 08:23:12

from __future__ import print_function
import sys
import os
from Tkinter import *
from lib import *
from mixin import *
from maker import *


class ShellGui(GuiMixin, GuiMakerWindowMenu):

    def start(self):
        self.setMenuBar()
        self.setToolBar()
        self.master.title('Shell Tool Listbox')
        self.master.iconname('Shell Tools')

    def handleList(self, event):
        label = self.listbox.get(ACTIVE)
        self.runCommand(label)

    def makeWidgets(self):
        sbar = Scrollbar(self)
        list = Listbox(self, bg='white')
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        for (label, action) in self.fetchCommands():
            list.insert(END, label)
        list.bind('<Double-1>', self.handleList)
        self.listbox = list

    def forToolBar(self, label):
        return True

    def setToolBar(self):
        self.toolBar = []
        for (label, action) in self.fetchCommands():
            if self.forToolBar(label):
                self.toolBar.append(label, action, dict(side=LEFT))
        self.toolBar.append('Quit', self.quit, dict(side=RIGHT))

    def setMenuBar(self):
        toolEntries = []
        self.menuBar = [
            ('File', 0, [('Quit', -1, self.quit)]),
            ('Tools', 0, toolEntries)
        ]
        for (label, action) in self.fetchCommands():
            toolEntries.append(label, -1, action)


class ListMenuGui(ShellGui):

    def fetchCommands(self):
        return self.myMenu

    def runCommand(self, cmd):
        for (label, action) in self.myMenu:
            if label == cmd:
                action()


class DictMenuGui(ShellGui):

    def fetchCommands(self):
        return self.myMenu.items()

    def runCommand(self):
        self.myMenu[cmd]()

