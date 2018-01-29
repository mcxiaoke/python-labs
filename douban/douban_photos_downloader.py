#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-24 17:24:26
from __future__ import print_function, unicode_literals, absolute_import
import requests
import json
import os
import sys
import hashlib
import time
import argparse
import logging
from lxml import etree, html

logging.basicConfig(level=logging.INFO)

__version__ = '1.0.0'

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Douban Photos Downloader v{0}'.format(__version__),
        epilog='''https://github.com/mcxiaoke/python-labs
        ''')
    parser.add_argument('-a', '--album',
                        help='Album Id')
    parser.add_argument('-l', '--doulist',
                        help='Doulist Id')
    parser.add_argument('-u', '--userid',
                        help='User Id')
    parser.add_argument('-o', '--output',
                        help='Save Destination')
    parser.add_argument('web_url', help='Download from douban url')
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return args

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    args = vars(parse_args())
    print(args)

### smart download by url 
# ref: https://www.douban.com/note/206320326/
# user photos url
# doulist albums url
# album photos url
# suject photos url
# online photos url
# celebrity photos url
# douban note url
# general web page url
### generating simple gallery page