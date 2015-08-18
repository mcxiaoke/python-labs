#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-18 20:14:05

INVALID_CHARS='/\\<>:?*"|'
def get_safe_filename(text):
    text=text.replace(':', 'x')
    for c in INVALID_CHARS:
        if c in text:
            text = text.replace(c, "_")
