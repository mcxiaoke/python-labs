# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


class User:
    def __init__(self, id, username, password, created_at, created_ip):
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at
        self.created_ip = created_ip
