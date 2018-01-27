# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/4 23:30.
__author__ = 'mcxiaoke'

# set

st = {'hello', 'world', '2015'}
st2 = {'hello', 'cat', 'dog', '2018'}
print len(st)  # out:3
# 判断元素是否存在
print 'hello' in st  # out:True
print 'cat' not in st  # out:True
# 判断超集和子集
print st.issubset(st2)  # out:False
print st.issubset({'hello', 'world', '2015', 'animals'})  # out:True
print st.issuperset({'2015'})  # out:True
print st.issubset(st)  # out:True
print st.issuperset(st)  # out:True
# 并集
print st.union(st2)  # out:set(['2018', '2015', 'world', 'dog', 'hello', 'cat'])
# 差集
print st.difference(st2)  # out:set(['2015', 'world'])
# 从其它set更新
st.update(st2)
print st  # out:set(['2018', '2015', 'world', 'dog', 'hello', 'cat'])
# 移除其它set中存在的
st.difference_update(st2)
print st  # out:set(['2015', 'world'])
st = {'hello', 'cat', '2018', 'weather'}
# 保存其它set中存在的
st.symmetric_difference_update(st2)
print st  # out:set(['weather', 'dog'])

# 添加删除
st = {'hello', 'cat', '2018', 'weather'}
st.add('hello')
st.add('dog')
print st  # out:set(['dog', 'hello', 'weather', '2018', 'cat'])
st.remove('weather')
st.discard('2018')
print st  # out:set(['dog', 'hello', 'cat'])
st.discard({'dog', 'cat'})
print st  # out:set(['cat'])
st = {'hello', 'cat', '2018', 'weather'}
st.pop()
st.pop()
print st  # out:set(['2018', 'cat'])
st.clear()
print st  # out:set([])

# dict

# 构造方式
d1 = dict(one=1, two=2, three=3)
d2 = {'one': 1, 'two': 2, 'three': 3}
d3 = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d4 = dict([('one', 1), ('two', 2), ('three', 3)])
d5 = dict({'three': 3, 'one': 1, 'two': 2})
print d1 == d2 == d3 == d4 == d5  # out:True
print d5  # out:{'three': 3, 'two': 2, 'one': 1}

# 操作方法
print len(d1)  # out:3
print d1['one']  # out:1
print d1.get('one')  # out:1
print d1.has_key('four')  # out:False
d1['one'] = 'one'
print d1  # out:{'three': 3, 'two': 2, 'one': 'one'}
print d2 == d1  # out:False
print 'one' in d1  # out:True
print 'one' not in d2  # out:False
d3.clear()  #
print len(d3)  # out:0
print d3 == {}  # out:True
print d2.items()  # out:[('three', 3), ('two', 2), ('one', 1)]
print d2.keys()  # out:['three', 'two', 'one']
print d2.values()  # out:[3, 2, 1]
print d2.pop('one')  # out:1
print d2  # out:{'three': 3, 'two': 2}
d1 = dict(one=1, two=2, three=3)
keys = d1.viewkeys()
print keys  # out:dict_keys(['three', 'two', 'one'])
d1['four'] = 4
print keys  # out:dict_keys(['four', 'three', 'two', 'one'])
