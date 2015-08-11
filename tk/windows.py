#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 11:17:56

from __future__ import print_function
import sys
import os
import glob
from Tkinter import *
from lib import *
from mixin import *
from maker import *
from tkSimpleDialog import *
from tkMessageBox import *


class _window:

    '''
    mixin shared by main and popup windows
    '''
    foundicon = None
    iconpatt = '*.ico'
    iconmine = 'py.ico'

    def configBorders(self, app, kind, iconfile):
        if not iconfile:
            iconfile = self.findIcon()
        title = app
        if kind:
            title = ' - '+kind
        self.title(title)
        self.iconname(app)
        if iconfile:
            try:
                self.iconbitmap(iconfile)
            except Exception, e:
                pass
        self.protocol('WM_DELETE_WINDOW', self.quit)

    def findIcon(self):
        if _window.foundicon:
            return _window.foundicon
        iconfile = None
        iconshere = glob.glob(self.iconpatt)
        if iconshere:
            iconfile = iconshere[0]
        else:
            mymod = __import__(__name__)
            path = __name__.split('.')
            for mod in path[1:]:
                mymod = getattr(mymod, mod)
            mydir = os.path.dirname(mymod.__file__)
            myicon = os.path.join(mydir, self.iconmine)
            if os.path.exists(myicon):
                iconfile = myicon
        _window.foundicon = iconfile
        return iconfile


class MainWindow(Tk, _window):
    # run in main top level window

    def __init__(self, app, kind='', iconfile=None):
        Tk.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)

    def quit(self):
        if self.okayToQuit():
            if askyesno(self.__app, 'Verify Quit Proram?'):
                self.destroy()
        else:
            showinfo(self.__app, 'Quit not allowed')

    def destroy(self):
        Tk.quit(self)

    def okayToQuit(self):
        return True


class PopupWindow(Toplevel, _window):
    # run in secondary popup window

    def __init__(self, app, kind='', iconfile=None):
        Toplevel.__init__(self)
        self.__app = app
        self.configBorders(app, kind, iconfile)

    def quit(self):
        if askyesno(self.__app, 'Verify quit Windows?'):
            self.destroy()

    def destroy(self):
        Toplevel.destroy(self)


class QuietPopupWindow(PopupWindow):

    def quit(self):
        self.destroy()


class ComponentWindow(Frame):
    # attched to another display

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.config(relief=RIDGE, border=2)

    def quit(self):
        showinfo('Quit', 'Not supported in attchment mode')


def _self_test():
    class Content:

        def __init__(self):
            Button(self, text='Hello', command=self.quit).pack()
            Button(self, text='World', command=self.destroy).pack()

    class ContentMix(MainWindow, Content):

        def __init__(self):
            MainWindow.__init__(self, 'mixin', 'Main')
            Content.__init__(self)
    main = ContentMix()
    main.minsize(320,240)

    class ContentMix2(PopupWindow, Content):

        def __init__(self):
            PopupWindow.__init__(self, 'mixin', 'Popup')
            Content.__init__(self)

    popup = ContentMix2()
    popup.minsize(320,240)

    class ContentMix3(ComponentWindow, Content):

        def __init__(self):
            ComponentWindow.__init__(self, popup)
            Content.__init__(self)

    ContentMix3()

    class ContentSubclass(PopupWindow):

        def __init__(self):
            PopupWindow.__init__(self, 'popup', 'Subclass')
            Button(self, text='PopupA', command=self.quit).pack()
            Button(self, text='PopupB', command=self.destroy).pack()

    sub = ContentSubclass()
    sub.minsize(320,240)

    win = PopupWindow('popup', 'Attachment')
    win.minsize(320,240)
    Button(win, text='Redwood', command=win.quit).pack()
    Button(win, text='Sing', command=win.destroy).pack()

    mainloop()

if __name__ == '__main__':
    _self_test()
