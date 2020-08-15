#!/bin/env python3
import csv
import sys
from datetime import datetime

rows = []

with open(sys.argv[1]) as f:
    fc = csv.reader(f)
    headers = next(fc)
    for r in fc:
        di = datetime.strptime(r[0], '%Y-%m-%d')
        r_date = datetime.strftime(di, '%m/%d/%y')
        r_account = '现金'
        r_cate = r[3]
        if r_cate == '零食烟酒':
            r_cate = '零食'
        r_tag = ''
        r_out = r[5]
        r_in = '0'
        r_type = 'CNY'
        r_out2 = r[5]
        r_type2 = 'CNY'
        r_comment = r[4] + ' - '+r[7]
        new_row = (r_date, r_account, r_cate, r_tag, r_out,
                   r_in, r_type, r_out2, r_type2, r_comment)
        # print(r)
        print(new_row)
        rows.append(new_row)

# "日期","账户","类别","标签","支出金额","收入金额","货币","以主要货币","主要货币","说明"
# ('08/13/20', '现金', '零食', '', '35.50', '0', 'CNY', '35.50', 'CNY', '饮料 - 超市买纯净水M')
with open('to.csv', 'w') as f:
    fc = csv.writer(f)
    fc.writerow(('日期', '账户', '类别', '标签', '支出金额',
                 '收入金额', '货币', '以主要货币', '主要货币', '说明'))
    for r in rows:
        fc.writerow(r)
