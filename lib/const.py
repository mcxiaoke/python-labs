#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import, print_function
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY35 = sys.version_info[0:2] >= (3, 5)
PYPY = 'pypy' in sys.version.lower()
OS_WIN = 'win32' in str(sys.platform).lower()

ASCII_CHARS = set(chr(x) for x in range(128))
URL_SAFE = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
               'abcdefghijklmnopqrstuvwxyz'
               '0123456789' '#' '_.-/~')
IRI_UNSAFE = ASCII_CHARS - URL_SAFE

DEFAULT_REQUEST_TIMEOUT = 30
USER_AGENT_OSX = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.3239.132 Safari/537.36'
USER_AGENT_WIN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.2743.116 Safari/537.36 Edge/15.15063'
USER_AGENT_FIREFOX = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/87.0'
USER_AGENT_MOBILE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/14.0 Mobile/15C202 Safari/604.1'