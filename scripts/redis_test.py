#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2018-01-31
from __future__ import print_function, absolute_import
import codecs
import requests
import base64
import json
import sys
import os
import re
import time
import shutil
import random
import json
import redis

r = redis.StrictRedis(decode_responses=True)

r.set(u'name', u'名字哈哈哈')
v = r.get(u'name')
print(type(v))
print(v)