import csv
import sys

'''
['2019/8/3', '现金', '食物', '', '33.50', '0', 
'CNY', '33.50', 'CNY', '网上京客隆蔬菜饮料雪糕']

d[0] time
d[2] category
d[4] amount
d[9] desc
'''
rows = []

with open(sys.argv[1]) as f:
    fc = csv.reader(f)
    headers = next(fc)
    for r in fc:
        rows.append((r[0],r[2],r[4],r[9]))

# ('2019/8/3', '食物', '33.50', '网上京客隆蔬菜饮料雪糕')
with open('out.csv', 'w') as f:
    fc = csv.writer(f)
    for r in rows:
        nr = ('信用卡',r[2], r[0], r[1], '人民币', '不可报销', r[3])
        fc.writerow(nr)