# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

def adder(n):
    n+=100
    yield n

for i in adder(10):
    print i