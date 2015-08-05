#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 07:49:55

from fanfou import FanfouClient


# requests
# oauth2
# requests-oauthlib
#

if __name__ == '__main__':
    client = FanfouClient()
    print client.login("test", "test")
    # print client.verify()
    print client.get_user("androidsupport",mode="lite", format="txt")
