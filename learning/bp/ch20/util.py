# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


def lines(file):
    for line in file:
        yield line
        yield '\n'


def blocks(file):
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
