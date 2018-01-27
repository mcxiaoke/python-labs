print "hello,world!"

x = 0
if x < 0:
    print "x<0"
elif x > 0:
    print "x>0"
else:
    print 'x=0'

for a in [1, 23, 4343.343, 'fdsfds', 'fdsf34']:
    print "a is ", a

idx=range(5)
print 'range is', idx

i = 0
while i < 10:
    print i*i
    i += 1

for m in range(10):
    if m == 2:
        continue
    else:
        print m*m*m


def square_sum(a,b):
    return a*b,b*b,a*a+b*b

print square_sum(3,4)

def change_list(list):
    list[0] = 'changed'

list=[34234,34324.324,4324,'fdfd']

print list
change_list(list)
print list

class User(object):
    name='User'
    male=True
    age=20

    def __init__(self):
        print 'user __init__'

    def hello(self):
        print 'Hello! I am',self.name

    def walk_to(self,target):
        print 'I am walking to ', target

class Engineer(User):
    def __init__(self):
        self.name='engineer'
        print('engineer init')


u=User()
print u.name
u.hello()
u.walk_to('office')

e=Engineer()
print(e.name)
e.hello()
