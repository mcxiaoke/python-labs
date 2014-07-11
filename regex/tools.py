# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import re
import sys

URL_PATTERN = r'www.douban.com/people/(\w+?)/'
FILE_OUTPUT = 'data/seeds.txt'


def extract_ids(filename):
    matches = re.findall(URL_PATTERN, open(filename).read())
    if not matches:
        print 'no ids found, quit.'
    with open(FILE_OUTPUT, 'w') as f:
        for uid in matches.sort():
            f.write(uid + '\n')
    print 'all ids is extracted from raw data.'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        extract_ids(sys.argv[1])
    else:
        print 'please set raw data file'

