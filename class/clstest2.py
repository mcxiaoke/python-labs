# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


class EmptyClass:
    pass


ec = EmptyClass()
ec.power = lambda x: x * x
ec.name = "empty class"
print ec.power(100)
print type(ec.power)
print type(lambda x: x * x)
