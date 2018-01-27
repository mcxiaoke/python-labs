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