#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 20:07:34
import sqlite3

from db_config import USER_TABLE_CREATE_SQL
from db_config import STATUS_TABLE_CREATE_SQL
import utils
from basedb import BaseDB


class DB(BaseDB):

    def __init__(self, db_name):
        super(DB, self).__init__(db_name)
        self._create_tables()

    def _create_tables(self):
        conn = self.conn
        conn.execute(USER_TABLE_CREATE_SQL)
        conn.execute(STATUS_TABLE_CREATE_SQL)
        conn.commit()

    def get_user_count(self):
        return self.get_count('user')

    def get_status_count(self):
        return self.get_count('status')

    def get_all_user_ids(self):
        rows = self.execute('select id from user').fetchall()
        ids = [row['id'] for row in rows]
        return ids

    def get_all_status_ids(self):
        rows = self.execute('select id from status').fetchall()
        ids = [row['id'] for row in rows]
        return ids

    def get_all_users(self):
        return self.fetch_all('user')

    def get_all_status(self):
        return self.fetch_all('status')

        # oldest user order by creation time
    def get_oldest_user(self):
        c = self.execute("select id,screen_name,created_at from user "
                         "order by created_at ASC limit 1;")
        return c.fetchone()

        # oldest status order by creation time
    def get_oldest_status(self):
        c = self.execute("select id,sid,uid,created_at from status "
                         "order by created_at ASC limit 1;")
        return c.fetchone()

        # latest user order by creation time
    def get_latest_user(self):
        c = self.execute("select id,screen_name,created_at from user "
                         "order by created_at DESC limit 1;")
        return c.fetchone()

        # latest status order by creation time
    def get_latest_status(self):
        c = self.execute("select id,sid,uid,created_at from status " +
                         "order by created_at DESC limit 1;")
        return c.fetchone()

    def insert_user(self, user):
        values = utils.convert_user(user)
        c = self.conn.cursor()
        c.execute(("INSERT OR REPLACE INTO user "
                   " (id,screen_name,created_at,added_at,data) "
                   " VALUES (?,?,?,?,?) "), *values)
        print "insert_user: %d rows inserted to db" % c.rowcount
        self.conn.commit()
        return c

    def bulk_insert_user(self, user_list):
        values = [utils.convert_user(user) for user in user_list]
        c = self.conn.cursor()
        c.executemany(("INSERT OR REPLACE INTO user "
                       " (id,screen_name,created_at,added_at,data) "
                       " VALUES (?,?,?,?,?) "), values)
        print "bulk_insert_user: %d rows inserted to db" % c.rowcount
        self.conn.commit()
        return c

    def insert_status(self, status):
        values = utils.convert_status(status)
        c = self.conn.cursor()
        c.execute(("INSERT OR REPLACE INTO status "
                   " (id,sid,uid,created_at,added_at,data) "
                   " VALUES (?,?,?,?,?,?) "), *values)
        self.conn.commit()
        print "insert_status: %d rows inserted to db" % c.rowcount
        return c

    def bulk_insert_status(self, status_list):
        values = [utils.convert_status(status) for status in status_list]
        c = self.conn.cursor()
        c.executemany(("INSERT OR REPLACE INTO status "
                       " (id,sid,uid,created_at,added_at,data) "
                       " VALUES (?,?,?,?,?,?) "), values)
        self.conn.commit()
        print "bulk_insert_status: %d rows inserted to db" % c.rowcount
        return c

    def print_status(self):
        # print 'users count:', self.get_user_count()
        # print 'oldest user:', self.get_oldest_user()
        # print 'latest user:', self.get_latest_user()
        print 'status count:', self.get_status_count()
        print 'oldest status:', self.get_oldest_status()
        print 'latest status:', self.get_latest_status()


if __name__ == '__main__':
    db = DB("test.db")
    db.print_status()
    db.close()
