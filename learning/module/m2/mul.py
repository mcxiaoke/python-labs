# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


def fib(n):
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a + b
