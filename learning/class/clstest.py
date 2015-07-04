# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


class MyClass:
    """A simple demo class"""
    i = 1000

    @staticmethod
    def same():
        print "static method"

    @classmethod
    def name(cls):
        print "I am a class method!"

    def __init__(self):
        self.data = []

    def hello(self):
        self.data.append("H")
        print "Hello, ", self.__doc__

class SecondClass(MyClass):
    """A simple inheritance class"""

    def hello2(self):
        print "Hello, Second class, hahaah"


cls = SecondClass()
MyClass.name()
hello = cls.hello
hello()
cls.hello2()