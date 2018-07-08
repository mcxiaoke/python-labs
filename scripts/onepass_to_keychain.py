#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import csv
from urlparse import urlparse, urlunparse

XML_TPL = '''
<xml>
<entries ext="Password Exporter" extxmlversion="1.1" type="saved" encrypt="false">
{}
</entries>
</xml>
'''
ENTRY_TPL = '''
<entry host="{}" user="{}" password="{}" formSubmitURL="{}" httpRealm="" userFieldName="userName" passFieldName="password"/>
'''


def main():
    entries = []
    with open(sys.argv[1], 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            username = row[3]
            password = row[2]
            url = row[4]
            up = urlparse(url)
            host= '{}://{}'.format(up.scheme, up.netloc)
            print(host)
            entry = ENTRY_TPL.format(host, username, password, host)
            entries.append(entry)
    if entries:
        entries_string = ''.join(entries)
        xml_string = XML_TPL.format(entries_string)
        with open('test.xml', 'wb') as f:
            f.write(xml_string)


if __name__ == '__main__':
    main()
