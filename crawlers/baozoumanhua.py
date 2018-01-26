# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-26 12:40:35
# @Last Modified by:   mcxiaoke
# @Last Modified time: 2018-01-26 12:40:42
from __future__ import print_function, unicode_literals, absolute_import
import codecs
import base64
import json
import sys
import os
import re
import time
import shutil
import random
import argparse
import traceback
import requests
import bs4
from bs4 import BeautifulSoup
from lxml import etree

def main():
    url = 'http://baozoumanhua.com/catalogs/gif?page=1'
    r = commons.get(url)
    text = r.text

if __name__ == '__main__':
    sys.path.insert(1, os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))))
    from lib import commons
    main()

