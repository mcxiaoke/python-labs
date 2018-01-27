#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-10 21:25:48
from __future__ import print_function
import sys
import os
from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog import asksaveasfilename
from tkMessageBox import askquestion, askyesno
from tkMessageBox import showerror, showinfo, showwarning

def  frame(root,side=TOP,**extras):
    widget=Frame(root)
    widget.pack(side=side,expand=YES,fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget

def label(root,side,text,**extras):
    widget=Label(root,text=text,relief=RIDGE)
    widget.pack(side=side,expand=YES,fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget

def button(root,side,text,command,**extras):
    widget=Button(root,text=text,command=command)
    widget.pack(side=side,expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget

def entry(root,side,linkvar,**extras):
    widget=Entry(root,relief=SUNKEN, textvariable=linkvar)
    widget.pack(side=side,expand=YES,fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget

def widgets_demo():
    app=Tk()
    frm=frame(app,TOP)
    label(frm,LEFT,'SPAM')
    button(frm,BOTTOM,'Press',lambda: print('Pushed'))
    mainloop()

widgets_demo()
