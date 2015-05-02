#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests

__author__ = 'mcxiaoke'

from hashlib import md5
from string import lower
from  datetime import datetime
import time
import json

SEND_URL = "http://msg.umeng.com/api/send"
APP_KEY = "534f7d2a56240bc9d2027380"
APP_MESSAGE_SECRET = "089f4690dbf4ecaaf487d216d70fe9c8"
APP_MASTER_SECRET = "ahxctjbnslfh43ivphygbq83ucblkyy4"

MESSAGE_TYPE_UNICAST = "unicast"
MESSAGE_TYPE_BROADCAST = "broadcast"
DISPLAY_TYPE_MESSAGE = "message"
DISPLAY_TYPE_NOTIFICATION = "notification"


class DictEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)


class Base:
    def __init__(self):
        pass

    def to_dict(self):
        d = dict()
        s_dict = self.__dict__
        for k, v in s_dict.items():
            if v is None:
                del s_dict[k]
            elif hasattr(v, "to_dict"):
                d[k] = v.to_dict()
            else:
                d[k] = v
        return d


class Content(Base):
    def __init__(self, nid, id, title, text, type):
        self.nid = nid
        self.id = id
        self.title = title
        self.text = text
        self.type = type


class Body(Base):
    def __init__(self, custom):
        self.custom = custom


class Message(Base):
    def __init__(self, body, app_key=APP_KEY, type=MESSAGE_TYPE_BROADCAST,
                 display_type=DISPLAY_TYPE_MESSAGE, alias=None, device_tokens=None):
        self.appkey = app_key
        self.timestamp = str(int(time.time()))
        text = lower(self.appkey) + lower(APP_MASTER_SECRET) + self.timestamp
        self.validation_token = md5(text).hexdigest()
        self.type = type
        self.alias = alias
        self.device_tokens = device_tokens
        self.payload = {'body': body, 'display_type': display_type}


def skip_none(dc):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # d.iteritems isn't used as you can't del or the iterator breaks.
    for key, value in dc.items():
        if value is None:
            del dc[key]
        elif isinstance(value, dict):
            skip_none(value)
    return dc  # For convenience


def format_time(dt):
    return unicode(datetime.strftime(dt, "%m-%d %H:%M:%S"))


def send_message():
    content = Content(1234567890, 103013, u"我是推送通知的标题", u"我是推送文本内容 " + format_time(datetime.now()), 1001)
    body = Body(content)
    message = Message(body)
    data = json.dumps(message, cls=DictEncoder, sort_keys=True)
    print data
    r = requests.post(SEND_URL, data=data)
    print r.text


"""
umeng push message send tool

http://dev.umeng.com/message/android/api-server-doc
http://dev.umeng.com/message/android/integration-guide
http://dev.umeng.com/message/android/faq
"""
if __name__ == "__main__":
    send_message()



