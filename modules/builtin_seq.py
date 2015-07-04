# -*- coding: UTF-8 -*-
# Created by mcxiaoke on 15/7/4 21:54.
__author__ = 'mcxiaoke'

# 序列类型
# 主要包括 str, unicode, list, tuple, bytearray, buffer, xrange

# 序列支持的操作
s = [124, 543, 56, 9, 56, 'A', 'hello']
t = ['hello', 'world', 'A', 2015, 3.1415926]
# x in s # 测试元素x是否在序列s中
print 2015 in s  # False
print 123 in s  # True
# x not in s #测试元素x是否不在序列s中
print 2015 not in s  # True
# s + t #合并序列s和序列t，并集
print [100, 3.14] + ['hello', 2257, 9]  # out: [100, 3.14, 'hello', 2257, 9]
# s * n, n * s # 序列s的n倍元素浅拷贝
print [1, 3.13, 'A'] * 3  # out: [1, 3.13, 'A', 1, 3.13, 'A', 1, 3.13, 'A']
print [[]] * 4  # out:[[], [], [], []]
# s[i] #序列的第i个元素
print 's[2]=', s[2], 's[6]=', s[6]  # out: s[2]= 56 s[6]= hello

# s[i:j]	序列按索引i:j切片，返回子序列，区间[i,j)，前闭后开
# 注：如果i和j是负数，那么索引从序列尾部开始机选
# s = [124, 543, 56, 9, 56, 'A', 'hello']
print s[1:3]  # out: [543, 56]
print s[2:]  # out: [56, 9, 56, 'A', 'hello']
print s[:4]  # out: [124, 543, 56, 9]
# s[i:j:k] #序列按索引[i:j)切片，返回子序列，步进为k
ss = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
print ss[1:9:2]  # out: [2, 4, 6, 8]
print ss[1::3]  # out: [2, 5, 8, 11]
print ss[:6:2]  # out: [1, 3, 5]

# len(s) # 返回序列长度
print len(s)  # out:7
print len(t)  # out:5
print len(ss)  # out:11
# min(s) # 返回序列最小的元素
print min(s)  # out:9
print min(ss)  # out:1
# max(s) # 返回序列最大的元素
print max(s)  # out:hello
print max(ss)  # out:12

# s.index(x) # 返回元素x在序列s中的位置索引
print s.index(9)  # out:3
print s.index('hello')  # out:6
# s.count(x) # 返回元素x在序列s中出现的次数
print s.count(56)  # out:2
print s.count('A')  # out:1

# all(iterable)
# 测试是否这个序列的所有元素都是true
print all(s)  # out:True
print all(['', 'hello', 123])  # out:False
print all([0, 1, 2, 3])  # out:False

# any(iterable)
# 测试是否这个序列至少有一个元素为true
print any(s)  # out:True
print any(['', 'hello', 123])  # out:True
print any([0, 1, 2, 3])  # out:True
print any(['', 0, 0.0, False, None, [], {}, ()])  # out:False
print any([])  # out:False
print any([[], [], []])  # out:False

# 序列的修改操作
s = [1, 324, 35, 5, 435, 7, 99, 0, 28]
t = ['Aa', 'Bb', 'Cc', 'Dd']
# s[i] = x
# 赋值操作，修改序列s第i项的值为x
s[2] = 10002
print s  # out:[1, 324, 10002, 5, 435, 7, 99, 0, 28]
# s[i:j] = t
# 替换子序列[i:j)
s[1:3] = [101, 102, 103]
print s  # out:[1, 101, 102, 103, 5, 435, 7, 99, 0, 28]
# del s[i:j]	same as s[i:j] = []
# 删除子序列[i:j)
del s[1:3]
print s  # out:[1, 103, 5, 435, 7, 99, 0, 28]
# s[i:j:k] = t
# 替换子序列为序列t
# t的长度必须等于左边子序列的长度
s[1:5:2] = [11, 21]
print s  # out:[1, 11, 5, 21, 7, 99, 0, 28]
# del s[i:j:k]
# 删除子序列
del s[1:5:2]
print s  # out:[1, 5, 7, 99, 0, 28]
# s.append(x)
# 追加元素到尾部
s.append(2001)
print s  # out:[1, 5, 7, 99, 0, 28, 2001]
# s.extend(x)
# 追加元素到尾部
s.append(3001)
s.append(3001)
print s  # out:[1, 5, 7, 99, 0, 28, 2001, 3001,3001]
# s.count(x)
# 元素出现的次数
print s.count(3001)  # out:2
# s.index(x[, i[, j]])
# 元素位置索引
# 如果元素不存在，会抛异常
print s.index(2001)  # out:6
# s.insert(i, x) 等价于same as s[i:i] = [x]	(5)
# 插入元素
# 如果 i<0,i=i+len(s)
s.insert(3, 33333)
print s  # out:[1, 5, 7, 33333, 99, 0, 28, 2001, 3001, 3001]
# s.pop([i]) 等价于same as x = s[i]; del s[i]; return x	(6)
# 删除并返回元素，默认删除最后一个元素
print s.pop(3)  # out:33333
print s  # out:[1, 5, 7, 99, 0, 28, 2001, 3001, 3001]
# s.remove(x) 等价于  del s[s.index(x)]	(4)
# 删除元素，一次删除一个
s.remove(3001)
print s  # out:[1, 5, 7, 99, 0, 28, 2001, 3001]
# s.reverse()
# 就地反转序列
s.reverse()
print s  # out:[3001, 2001, 28, 0, 99, 7, 5, 1]
# s.sort([cmp[, key[, reverse]]])
# 序列排序，稳定排序
s.sort()
print s  # out:[0, 1, 5, 7, 28, 99, 2001, 3001]
