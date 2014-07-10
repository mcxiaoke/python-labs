# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


class Haha:
    x = 100

    def __init__(self):
        self.data = None

    def hello(self, name):
        print 'hello', name

    def set_data(self, data):
        self.data = data

    def display(self):
        print self.data


def aaa():
    x = 100
    print x


ha = Haha()
ha.hello('test1')
Haha.hello(ha, 'test2')
print Haha.x
ha.set_data('i am data')
ha.data = 'i am not data'
ha.test = 'test'
ha.display()
print ha.test

aaa.x=1000
print aaa.x
aaa()
