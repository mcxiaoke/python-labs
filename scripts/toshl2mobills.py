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
        c = r[2]
        if c in ('早餐', '晚餐', '午餐'):
            c = 'Eating'
        elif c in ('日常'):
            c = 'Shopping'
        elif c in ('衣物'):
            c = 'Clothing'
        elif c in ('数码'):
            c = 'Digital Products'
        elif c in ('生活'):
            c = 'Home'
        elif c in ('零食', '食物'):
            c = 'Food'
        elif c in ('汽车'):
            c = 'Car'
        elif c in ('交通'):
            c = 'Transportation'
        elif c in ('娱乐'):
            c = 'Entertainment'
        elif c in ('转账', '转帐'):
            c = 'Payments'
        elif c in ('其它'):
            c = 'Others'
        elif c in ('旅游'):
            c = 'Travel'
        elif c in ('宠物'):
            c = 'Pet'
        elif c in ('医疗'):
            c = 'Health'
        elif c in ('房租'):
            c = 'House'
        elif c in ('投资'):
            c = 'Investment'
        else:
            print('Ignore:', r)
            c = None
        if c:
            # print(r[4])
            d = datetime.strptime(r[0], '%m/%d/%y')
            dt = datetime.strftime(d, '%d/%m/%Y')
            m = float(r[4].replace(',', '')) * -1
            rows.append((dt, c, m, '{} ({})'.format(r[9], r[2])))

# ('2019/8/3', '食物', '33.50', '网上京客隆蔬菜饮料雪糕')
with open('mobills.csv', 'w') as f:
    fc = csv.writer(f)
    fc.writerow(('Date', 'Description', 'Amount', 'Account', 'Category'))
    # fc = csv.writerow(f)
    for r in rows:
        nr = (r[0], r[1], r[2], 'Wallet', r[3])
        # print(nr)
        fc.writerow(nr)
