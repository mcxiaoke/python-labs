#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 21:04:24
DB_NAME = "fanfou.db"

USER_TABLE = "user"
STATUS_TABLE = "status"

USER_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS user '
    ' ( _id INTEGER PRIMARY KEY, '
    ' id TEXT, '
    ' screen_name TEXT, '
    ' created_at INTEGER, '
    ' added_at INTEGER, '
    ' data TEXT, '
    ' UNIQUE (id) ); '
)

STATUS_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS status '
    ' ( _id INTEGER PRIMARY KEY, '
    ' id TEXT, '
    ' rid INTEGER, '
    ' uid TEXT,'
    ' created_at INTEGER, '
    ' added_at INTEGER, '
    ' data TEXT, '
    ' UNIQUE (rid) ); '
)


'''
http://stackoverflow.com/questions/6237378/insert-into-sqlite-table-with-unique-column
http://sqlite.org/lang_insert.html
http://zetcode.com/db/sqlite/constraints/
http://www.pythoncentral.io/introduction-to-sqlite-in-python/
http://www.runoob.com/sqlite/sqlite-constraints.html
http://www.cnblogs.com/myqiao/archive/2011/07/13/2105550.html
'''

if __name__ == '__main__':
    print "database config file"
