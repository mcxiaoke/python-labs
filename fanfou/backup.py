#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-06 07:23:50

import fanfou
import utils
import time
import sys
from db import DB

DEFAULT_COUNT = 60


def fetch_newer_statuses(api, uid):
    # first ,check new statuses
    db = DB('%s.db' % uid)
    head_status = db.get_latest_status()
    if head_status:
        while(True):
            head_status = db.get_latest_status()
            since_id = head_status['sid'] if head_status else None
            print 'fetch timeline, since_id: %s' % since_id
            timeline = api.get_user_timeline(
                uid, count=DEFAULT_COUNT, since_id=since_id)
            if not timeline:
                break
            print len(timeline)
            db.bulk_insert_status(timeline)
            time.sleep(2)
            if len(timeline) < DEFAULT_COUNT:
                break
    db.print_status()


def fetch_older_statuses(api, uid):
    # then, check older status
    db = DB('%s.db' % uid)
    while(True):
        tail_status = db.get_oldest_status()
        max_id = tail_status['sid'] if tail_status else None
        print 'fetch timeline, max_id: %s' % max_id
        timeline = api.get_user_timeline(
            uid, count=DEFAULT_COUNT, max_id=max_id)
        if not timeline:
            break
        print len(timeline)
        db.bulk_insert_status(timeline)
        time.sleep(2)
        if len(timeline) < DEFAULT_COUNT:
            break
    db.print_status()


def main(username, password, userid=None):
    api = fanfou.FanfouClient()
    token = utils.load_account_info(username)
    if token:
        print 'load account info: %s for %s' % (
            token, username)
        api.set_oauth_token(token)
    else:
        print "no saved account info, get token from server..."
    if api.is_verified():
        token = api.oauth_token
        user = api.user
    else:
        token = api.login(username, password)
        user = api.user
        print 'save new account_info: {0}'.format(token)
        utils.save_account_info(username, token)
    target_id = userid if userid else user['id']
    target_user = api.get_user(target_id)
    if not target_user:
        print "target user: %s not exists" % target_id
        return
    print "prepare backup data for user: %s" % target_id
    # first ,check new statuses
    fetch_newer_statuses(api, target_id)
    # then, check older status
    fetch_older_statuses(api, target_id)


if __name__ == '__main__':
    args = utils.parse_args()
    main(args.username, args.password, args.userid)
