# -*- coding: utf-8 -*-

import sys
import re
import os
import codecs

if __name__ == "__main__":
    input = sys.argv[1]
    with codecs.open(input, encoding="gb18030") as f:
        fulltext = f.read()
        text = fulltext[:600]
        p = re.compile("\w\r\n\w")
        m = re.findall("\w\r\n\w", text)
        print(text)
        print(m)
        t2 = re.sub("\w(\r\n)\w", "", text)
        print(re.sub("[\r\n]+", "\r\n", t2))
