__author__ = 'mcxiaoke'

def gen():
    for i in range(4):
        yield i

gene=gen()
print(type(gene))
print(gene.next())
print(gene.next())
print(gene.next())

re=iter(range(10))

try:
    #for i in range(5):
    for i in range(20):
        print(re.next())
except StopIteration as e:
    print('here is the end: ',i)
else:
    print("next")
finally:
    print("finally")
print('hahahah')