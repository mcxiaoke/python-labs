__author__ = 'mcxiaoke'
with open('file.txt','w') as f:
    print(f.closed)
    f.write("new line")
print(f.closed)

class Context(object):
    def __init__(self,text):
        self.text=text

    def __enter__(self):
        self.text="I am enter..."
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.text="I am exited.."


with Context('Haha') as c:
    print(c.text)

print(c.text)

class bird(object):
    feather = True

class chicken(bird):
    fly = False
    def __init__(self, age):
        self.age = age

summer = chicken(2)

print(bird.__dict__)
print(chicken.__dict__)
print(summer.__dict__)

