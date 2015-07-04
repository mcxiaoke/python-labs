# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


def hello(text):
    print "hello", text


def add10(num):
    return num + 10


def sum2(L):
    print L
    if not L:
        return 0;
    else:
        return L[0] + sum2(L[1:])


# hello("world!")
# hello("python")
# print "result is", add10(100)
sum2.a = 'aaa'
print sum2.a
sum2([1, 3, 5, 6, 7, 9])

