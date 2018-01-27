#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-14 15:55:34
from __future__ import print_function


def hello(level):
    def decorator(func,*args, **kwargs):
        print('before hello',level)
        func(*args, **kwargs)
        print('after hello')
    return decorator


@hello(level=12345)
def print_me(first=None, *args, **options):
    print('this is func 1', first, args, options)

t=(1,2,3)
print_me(first='First',**dict({'key': 'value'}))
