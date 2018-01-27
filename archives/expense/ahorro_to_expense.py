#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2016-01-08 11:57:43
from __future__ import print_function, unicode_literals
import os
import sys
import shutil
import codecs
import time
import uuid
import json

TABLES = {
    '其它': '购物',
    '饮料': '零食',
    '日常用品': '日常',
    '礼金': '礼物',
    '晚餐': '餐饮',
    '午餐': '餐饮',
    '食物': '餐饮',
    '宠物': '母婴',
    '娱乐': '数码',
    '转账': '支付',
    '转帐': '支付',
    '水电气': '日常',
    '数码产品': '数码',
    '电话费': '日常',
    '房租': '租金',
}


def convert(infile, outfile):
    out = codecs.open(outfile, 'w', 'utf-8')
    csv = codecs.open('out.csv', 'w', 'utf-8')
    rs = []
    data = {
        'version': '1.1',
    }
    expenses = []
    data['expenses'] = expenses
    with codecs.open(infile, 'r', 'utf-8') as f:
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            if l.startswith('#') or '投资' in l:
                continue
            # 0 date,1 _,2 _,3 category,4 cost,5 detail
            s = l.split(',', 6)
            if len(s) < 6 or l.startswith('#'):
                continue

            uuid1 = str(uuid.uuid1()).upper()
            timezone = 'Asia/Shanghai'
            ti = time.strptime('{} 10:00:00'.format(s[0].strip()), '%Y/%m/%d %H:%M:%S')
            datetime = time.strftime('%Y-%m-%d %H:%M:%S', ti)
            category = TABLES.get(s[3].strip()) or s[3].strip()
            cost = s[4].strip()
            detail = s[5].strip()
            record = {}
            record['uuid'] = uuid1
            record['timezone'] = timezone
            record['datetime'] = datetime
            record['category'] = category
            record['cost'] = cost
            record['detail'] = detail
            expenses.append(record)

            r = '{},{},Asia/Shanghai,{},{}'.format(category, datetime, cost, detail)
            rs.append(r)

    json.dump(data, out)
    csv.write('Category,Date Time,Timezone,Cost,Detail\n')
    for r in rs:
        csv.write(r)
        csv.write('\n')
    csv.close()

if __name__ == '__main__':
    convert('in.csv', 'out.json')
