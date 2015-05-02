# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import mailtools

mailer = mailtools.SMTPMailer('smtp.126.com', port=25, username="zxk198597@126.com", password="wbsyxrc53")
mailer.send_plain(
    u'zxk198597@126.com',
    [u'mcxiaoke@gmail.com'],
    u'哇哈哈',
    u'this is a emial from bot'
)
