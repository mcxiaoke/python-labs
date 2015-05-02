#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'mcxiaoke'
__createdAt = '2014-10-22'

import re
import json

import mailtools

import requests
from bs4 import BeautifulSoup
from pync import Notifier


NOTIFIER_TITLE = "iPhone 6 到货提醒"
TARGET_URL = "http://www.10010.com/goodsdetail/111410108357.html"
PATTERN = re.compile(r'articleAmountList = (\[\{.*\}\]);')

COLOR_DICT = {
    u"9809120800036797": u"灰色版",
    u"9810072100598994": u"金色版",
    u"9809120800036795": u"银色版",
    "^": "",
}

SMTP_HOST = "smtp.126.com"
SMTP_USER = "zxk198597@126.com"
SMTP_PASS = ""
SMTP_TO = ['mcxiaoke@gmail.com']


def send_mail(title, message):
    mailer = mailtools.SMTPMailer(SMTP_HOST, port=25, username=SMTP_USER, password=SMTP_PASS)
    mailer.send_plain(SMTP_USER, SMTP_TO, title, message)


response = requests.get(TARGET_URL)
# print "StatusCode:", response.status_code
# print "Encoding:", response.encoding
html = response.text
soup = BeautifulSoup(html)
amounts = PATTERN.findall(html)[0]
data = json.loads(amounts)
for di in data:
    for k, v in COLOR_DICT.iteritems():
        di['articleSymbol'] = di['articleSymbol'].replace(k, v)

for di in data:
    amount = int(di['articleAmount'])
    scheduled = int(di['scheduledAmount'])
    if amount > 0 or scheduled > 0:
        model = di['articleSymbol']
        if 'PLUS' in model and u'金色' in model:
            title = NOTIFIER_TITLE
            message = di['articleSymbol'].encode('utf8') + "有货了，赶紧买！"
            Notifier.notify(message,
                            title=title, open=TARGET_URL)
            send_mail(title, message)
    print u'{0: <18}'.format(di['articleSymbol']), \
        "库存:", u'{0: <4}'.format(di['articleAmount']), \
        "到货:", u'{0: <4}'.format(di['scheduledAmount'])

