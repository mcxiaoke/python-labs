#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 08:58:09
from __future__ import print_function
import sys
import os
from Tkinter import *
from lib import *
from mixin import *
from maker import *
from tkSimpleDialog import *


class GuiOutput:
    font = ('courier', 10, 'normal')

    def __init__(self, parent=None):
        self.text = None
        if parent:
            self.popupnow(parent)

    def popupnow(self, parent=None):
        if self.text:
            return
        self.text = ScrolledText(parent or Toplevel())
        #self.text.config(font=self.font)
        self.text.pack()

    def write(self, text):
        self.popupnow()
        self.text.insert(END, str(text))
        self.text.see(END)
        self.text.update()

    def writelines(self, lines):
        for line in lines:
            self.write(line)


class GuiInput:

    def __init__(self):
        self.buf = ''

    def inputline(self):
        line = askstring('GuiInput', 'Enter input line + <crlf> (cancel=eof)')
        if line == None:
            return ''
        else:
            return line+'\n'

    def read(self, bytes=None):
        if not self.buf:
            self.buf = self.inputline()
        if bytes:
            text = self.buf[:bytes]
            self.buf = self.buf[bytes:]
        else:
            text = ''
            line = self.buf
            while line:
                text = text+line
                line = self.inputline()
        return text

    def readline(self):
        text = self.buf or self.inputline()
        self.buf = ''
        return text

    def readlines(self):
        lines = []
        while True:
            next = self.readline()
            if not next:
                break
            lines.append(next)
        return lines


def redirectGuiFunc(func, *pargs, **kargs):
    import sys
    saveStreams = sys.stdin, sys.stdout
    sys.stdin = GuiInput()
    sys.stdout = GuiOutput()
    sys.stderr = sys.stdout
    result = func(*pargs, **kargs)
    sys.stdin, sys.stdou = saveStreams
    return result


def redirectGuiShellCmd(command):
    def reader(input, output):
        while True:
            line = input.readline()
            if not line:
                break
            output.write(line)
    import os
    input = os.popen(command, 'r')
    output = GuiOutput()
    reader(input, output)


if __name__ == '__main__':
    def makeUpper():
        while True:
            try:
                line = raw_input('Line?')
            except Exception, e:
                break
            print(line.upper())
        print('end of file')

    def makeLower(input, output):
        while True:
            line = input.readline()
            if not line:
                break
            output.write(line.lower())
        print('end of file')

    root = Tk()
    Button(root, text='test streams ',
           command=lambda: redirectGuiFunc(makeUpper)).pack(fill=X)
    Button(root, text='test files ', command=lambda: makeLower(
        GuiInput(), GuiOutput())).pack(fill=X)
    Button(root, text='test popen ',
           command=lambda: redirectGuiShellCmd('dir *')).pack(fill=X)
    root.mainloop()

#p629
