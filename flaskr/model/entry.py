# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


class Entry:
    def __init__(self, title, abstract, text, user_id, created_at):
        self.title = title
        self.abstract = abstract
        self.text = text
        self.user_id = user_id
        self.created_at = created_at
