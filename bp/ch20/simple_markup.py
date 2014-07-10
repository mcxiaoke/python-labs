# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import sys

import re
from util import *


HEAD = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>...</title>
<head>
<body>
'''.strip()

print HEAD
title = True

for block in blocks(sys.stdin):
    block = re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
    if title:
        print '<h1>'
        print block
        print '</h1>'
        title = False
    else:
        print '<p>'
        print block
        print '<p>'

print '</body></html>'



