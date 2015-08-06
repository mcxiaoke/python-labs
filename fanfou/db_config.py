#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 21:04:24
DB_NAME = "fanfou.db"

KV_TABLE = "kv"
LOG_TABLE = "log"
USER_TABLE = "user"
STATUS_TABLE = "status"

KV_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS kv '
    ' ( _id INTEGER PRIMARY KEY, '
    ' key TEXT, '
    ' value TEXT, '
    ' comment TEXT, '
    ' added_at TEXT'
    ' UNIQUE (key) ); '
)

LOG_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS log '
    ' ( _id INTEGER PRIMARY KEY, '
    ' tag TEXT, '
    ' action TEXT, '
    ' message TEXT, '
    ' comment TEXT, '
    ' added_at TEXT'
    ' UNIQUE (_id) ); '
)

USER_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS user '
    ' ( _id INTEGER PRIMARY KEY, '
    ' id TEXT, '
    ' screen_name TEXT, '
    ' created_at TEXT, '
    ' added_at TEXT, '
    ' data TEXT, '
    ' UNIQUE (id) ); '
)

STATUS_TABLE_CREATE_SQL = (
    'CREATE TABLE IF NOT EXISTS status '
    ' ( _id INTEGER PRIMARY KEY, '
    ' id INTEGER, '
    ' sid TEXT, '
    ' uid TEXT,'
    ' created_at TEXT, '
    ' added_at TEXT, '
    ' data TEXT, '
    ' UNIQUE (id) ); '
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
