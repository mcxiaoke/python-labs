#-*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import cPickle as pickle

class Bird(object):
    have_feather = True
    hello = "hello"


summer=Bird()
ps=pickle.dumps(summer)
print summer.have_feather
print summer.hello

summer=pickle.loads(ps)
print summer.have_feather
print summer.hello

