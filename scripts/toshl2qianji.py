'''
File: toshl2qianji.py
Created: 2019-12-20 14:03:39
Modified: 2021-03-01 10:16:22
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''


import csv
import sys
from datetime import datetime

'''
tosh data row sample
"日期","账户","类别","标签","支出金额","收入金额","货币","以主要货币","主要货币","说明"
2021/2/28,现金,食物,,15.50,0,CNY,15.50,CNY,集贸市场买东西

qianji app row template
时间，分类，类型，金额，账户1，账户2，备注，账单图片
'''
rows = []

catogries = ['三餐', '食物', '零食', '衣物', '交通', '旅行', '宠物', '投资',
             '日用品', '住房', '医疗', '汽车', '娱乐', '数码', '其它', '生活', '转账']

with open(sys.argv[1]) as f:
    fc = csv.reader(f)
    headers = next(fc)
    index = 0
    r_type = '支出'
    for r in fc:
        r_date = r[0]
        if r[2] not in catogries:
            if r[2] in ('餐饮', '晚餐', '午餐', '早餐'):
                r_cato = '三餐'
            elif r[2] in ('转帐', '人情'):
                r_cato = '转账'
            elif r[2] in ('购物', '日常'):
                r_cato = '日用品'
            elif r[2] in ('通讯'):
                r_cato = '生活'
            elif r[2] == '房租':
                r_cato = '住房'
            elif r[2] in ('其他', '文教'):
                r_cato = '其它'
            else:
                r_cato = r[2]
        else:
            r_cato = r[2]
        r_amount = r[4].replace(',', '')
        r_note = r[9]
        if float(r_amount) < 1:
            r_amount = '1'
        q_row = (r_date, r_cato, r_type, r_amount, '', '', r_note, '')
        rows.append(q_row)

with open('/tmp/qianji-import.csv', 'w') as f:
    fc = csv.writer(f)
    # 时间,分类,类型,金额,账户1,账户2,备注,账单图片
    # 7/12/20 21:20,三餐,支出,28.58,微信,,去肯德基吃汉堡
    fc.writerow(('时间', '分类', '类型', '金额', '账户1', '账户2', '备注', '账单图片'))
    for r in rows:
        print('Write:{}'.format(r))
        fc.writerow(r)
