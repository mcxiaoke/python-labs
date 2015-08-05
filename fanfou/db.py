#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 20:07:34
import sqlite3

from db_config import DB_NAME
from db_config import USER_TABLE_CREATE_SQL
from db_config import USER_TABLE
from db_config import STATUS_TABLE_CREATE_SQL
from db_config import STATUS_TABLE
import json
import utils


class DB:

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self._check_db()

    def _check_db(self):
        c = self.conn.cursor()
        c.execute(USER_TABLE_CREATE_SQL)
        c.execute(STATUS_TABLE_CREATE_SQL)
        self.conn.commit()

    def execute(self, sql, parameters=None):
        c = self.conn.cursor()
        return c.execute(sql, parameters)


    def user_insert(self, user):
        id = user["id"]
        screen_name = user["screen_name"]
        created_at = utils.normalize_fanfou_date(user["created_at"])
        added_at = utils.get_now_datetime_str()
        data = json.dumps(user)
        c = self.conn.cursor()
        c.execute(("INSERT OR IGNORE INTO user "
                   " (id,screen_name,created_at,added_at,data) "
                   " VALUES (?,?,?,?,?) "),
                  id, screen_name, created_at, added_at, data)
        print c


if __name__ == '__main__':
    db = DB()
