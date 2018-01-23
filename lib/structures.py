#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division, absolute_import, print_function
import sqlite3

class ReadOnlyDict(dict):
    """A Read Only Dict"""

    def __setitem__(self, key, value):
        raise Exception("dict is read-only")


def getitem(obj, key=0, default=None):
    """Get first element of list or return default"""
    try:
        return obj[key]
    except:
        return default

class BaseDB(object):

    def __init__(self, db_name):
        self.name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

    def fetch_all(self, table_name):
        return self.conn.execute(
            'select * from %s;' % table_name).fetchall()

    def get_count(self, table_name):
        return self.conn.execute(
            'select count() from %s;' % table_name).fetchone()[0]

    def execute(self, operation):
        c = self.conn.cursor()
        c.execute(operation)
        self.conn.commit()
        return c