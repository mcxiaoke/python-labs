#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-09 16:04:45

#from tkinter.filedialog import askopenfilename
#from tkinter.colorchooser import askcolor
#from tkinter.messagebox import askquestion, showerror
#from tkinter.simpledialog import askfloat
from tkFileDialog import askopenfilename
from tkColorChooser import askcolor
from tkMessageBox import askquestion, showerror
from tkSimpleDialog import askfloat

#https://docs.python.org/2/library/tkinter.html

demos = {
    'Open': askopenfilename,
    'Color': askcolor,
    'Query': lambda: askquestion('Warning', 'Your typed "rm *"\nConfirm?'),
    'Error': lambda: showerror('Error!', "He's dead, Jim"),
    'Input': lambda: askfloat('Entry', 'Enter credit card number')

}
