__author__ = 'mcxiaoke'



def loginfo(pre=''):
    def decor(F):
        def new_F(a,b):
            print(pre+' input:',a,b)
            return F(a,b)
        return new_F
    return decor

@loginfo('func')
def square_sum(a,b):
    #print('square_sum input:',a,b)
    return a**2+b**2

@loginfo('func2')
def square_sub(a,b):
    #print('square_sub input:',a,b)
    return a**2-b**2


print(square_sum(3,4))
print(square_sub(3,4))

def decorator(aClass):
    class newClass:
        def __init__(self, age):
            self.total_display   = 0
            self.wrapped         = aClass(age)
        def display(self):
            self.total_display += 1
            print("total display", self.total_display)
            self.wrapped.display()
    return newClass

@decorator
class Bird:
    def __init__(self, age):
        self.age = age
    def display(self):
        print("My age is",self.age)

eagleLord = Bird(5)
for i in range(3):
    eagleLord.display()
