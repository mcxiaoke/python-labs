__author__ = 'mcxiaoke'

class Numm(object):
    def __init__(self,value):
        self.value=value

    def getNum(self):
        return self.value

    def setNum(self,value):
        self.value=value

    def delNum(self):
        print("value deleted.")
        del self.value
    nm=property(getNum,setNum,delNum,"set/get property")

x=Numm(14324)
print(x.nm)
x.nm=2323232
print(x.nm)
print(x.nm.__doc__)
del x.nm
print(x.__dict__)
print(x.nm)
