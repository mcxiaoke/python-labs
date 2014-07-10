# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

import sqlite3
import pprint

ZERO_FLOAT = float(0)
SOURCE_NAME = 'data.csv'
DB_NAME = 'data.db'
TABLE_NAME = 'data'
INSERT_SQL = 'INSERT INTO data VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'


def convert(value):
    if not value:
        value = '0'
        value.strip('\r\n')
    return float(value)


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(('\n'
                 '        CREATE TABLE IF NOT EXISTS data (\n'
                 '        id      INTEGER PRIMARY KEY,\n'
                 '        dt      TEXT,\n'
                 '        len     INTEGER,\n'
                 '        day1    FLOAT,\n'
                 '        day2    FLOAT,\n'
                 '        day3    FLOAT,\n'
                 '        day4    FLOAT,\n'
                 '        day5    FLOAT,\n'
                 '        day6    FLOAT,\n'
                 '        day7    FLOAT,\n'
                 '        day14   FLOAT,\n'
                 '        day30   FLOAT\n'
                 '        )\n'
                 '    '
    ))
    conn.commit()


def insert_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    index = 0
    for line in open(SOURCE_NAME):
        fields = line.split(',')
        if not fields[1].isdigit():
            continue
        field_count = len(fields)
        dt = fields[0]
        ln = int(fields[1])
        index += 1
        args = [index, dt, ln]
        for i in range(2, 11):
            if i < field_count:
                args.append(convert(fields[i]))
            else:
                args.append(ZERO_FLOAT)
        cur.execute(INSERT_SQL, args)
        conn.commit()


def get_all_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.execute('SELECT id,dt,len,day7 FROM data LIMIT 10')
    pprint.pprint(cur.fetchall())


if __name__ == "__main__":
    # create_table()
    # insert_data()
    get_all_data()