#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-25 08:45:45

from datetime import datetime

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
