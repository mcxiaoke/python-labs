__author__ = 'mcxiaoke'

def func1(a,b,c=10):
    return a+b+c

print(func1(1,2,3))

print(func1(c=3,b=11,a=5))

print(func1(2,c=3,b=4))

print(func1(2,4))
print(func1(2,4,6))

def func2(*name):
    print(type(name))
    print(name)

func2(1,4,6)
func2('fdsfsdf',4343,True)
func2([1,2,3])

aaa=(1,2,3,4,'34434')
func2(*aaa)
func2(aaa)

def func3(**kwargs):
    print(type(kwargs))
    print(kwargs)

func3(a=1,b=2)
func3(abc='fdfdsf',d=True,dddd=343434,ddd=124.3434)

dict = {'a':1,'b':2,'c':3}

func3(**dict)


