import csv
import sys
from datetime import datetime

'''
"日期","账户","类别","标签","支出金额","收入金额",

"货币","以主要货币","主要货币","说明"

['12/18/19', '现金', '食物', '', '24.00', '0', 
'CNY', '24.00', 'CNY', '月季园菜店买蔬菜']

d[0] date
d[9] desc
d[4] amount
d[2] category
'''
rows = []

with open(sys.argv[1]) as f:
    fc = csv.reader(f)
    headers = next(fc)
    for r in fc:
        d = datetime.strptime(r[0], '%m/%d/%y')
        dt = datetime.strftime(d, '%Y-%m-%d')
        rows.append((dt, r[2], r[4], r[9]))

# ('2019/8/3', '食物', '33.50', '网上京客隆蔬菜饮料雪糕')
with open('netease.csv', 'w') as f:
    fc = csv.writer(f)
    fc.writerow(('账户', '金额', '时间', '分类', '币种', '报销', '备注'))
    for r in rows:
        nr = ('信用卡', r[2], r[0], r[1], '人民币', '不可报销', r[3])
        fc.writerow(nr)
