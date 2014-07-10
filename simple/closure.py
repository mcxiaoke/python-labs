__author__ = 'mcxiaoke'

def line_conf():
    a=10
    def line(x):
        return x**2+a
    return line

a=100
ml=line_conf()
print(ml(5))
print(ml(10))
print(ml.__closure__)
print(ml.__closure__[0].cell_contents)

def line_conf(a, b):
    def line(x):
        return a*x + b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5))
print(line2(5))
