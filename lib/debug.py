from __future__ import unicode_literals, division, absolute_import, print_function
from const import OS_WIN, PY2

def log(s):
    if OS_WIN and PY2:
        if isinstance(s,str):
            print(s.decode('utf-8'))
        elif isinstance(s,unicode):
            # or s.encode('gbk', 'ignore')
            print(s.encode('gb18030'))
        else:
            print(s)
    else:
        print(s)