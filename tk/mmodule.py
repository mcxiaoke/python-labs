#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-11 10:40:48

from __future__ import print_function

count = 0

def message1():
    print('hello, message1 from module ')

def message2(self):
    print('hello, message2 from module 2 modified',count)
    self.method1()
