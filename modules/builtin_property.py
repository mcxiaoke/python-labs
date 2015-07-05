# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/5 17:00.
__author__ = 'mcxiaoke'

# property([fget[, fset[, fdel[, doc]]]])
class C1(object):
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x

    def setx(self, value):
        self._x = value

    def delx(self):
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")


class C2(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x


help(C1)
help(C2)
