__author__ = 'mcxiaoke'

class Bird(object):
    feather=True

class Chicken(Bird):
    fly=False

    def __init__(self,age):
        self.age=age

ck=Chicken(2)

print(Bird.__dict__)
print(Chicken.__dict__)
print(ck.__dict__)
