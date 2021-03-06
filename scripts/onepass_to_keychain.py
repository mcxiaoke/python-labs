#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import csv
from urllib.parse import urlparse, urlunparse

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
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            username = row[4]
            password = row[3]
            url = row[5]
            # print(url)
            up = urlparse(url)
            # print(up)
            host = '{}://{}'.format(up.scheme, up.netloc)
            print(host)
            entry = ENTRY_TPL.format(host, username, password, host)
            entries.append(entry)
    if entries:
        entries_string = ''.join(entries)
        xml_string = XML_TPL.format(entries_string)
        with open('keychain-import.xml', 'w') as f:
            f.write(xml_string)


if __name__ == '__main__':
    main()
