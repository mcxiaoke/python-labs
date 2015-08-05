#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 22:18:00

from datetime import datetime
import time

ISO_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FANFOU_DATE_FORMAT = "%a %b %d %H:%M:%S +0000 %Y"


def parse_fanfou_date(date_str):
    return datetime.strptime(date_str, FANFOU_DATE_FORMAT)


def normalize_fanfou_date(date_str):
    return normalize_datetime(parse_fanfou_date(date_str))


def parse_normalize_date(date_str):
    return datetime.strptime(date_str, ISO_DATE_FORMAT)


def normalize_datetime(dt):
    return dt.strftime(ISO_DATE_FORMAT)


def normalize_timestamp(ts):
    return normalize_datetime(datetime.fromtimestamp(ts))


def get_now_datetime_str():
    return normalize_datetime(datetime.now())

if __name__ == '__main__':
    date_str = "Sat May 12 14:24:26 +0000 2007"
    fd1 = parse_fanfou_date(date_str)
    fd2 = normalize_fanfou_date(date_str)
    nd1 = normalize_timestamp(time.time())
    nd2 = normalize_datetime(datetime.now())
    dt1 = parse_normalize_date(fd2)
    dt2 = parse_normalize_date(nd2)
    print fd1
    print fd2
    print dt1
    print nd1
    print nd2
    print dt2
    print normalize_datetime(datetime.now())
