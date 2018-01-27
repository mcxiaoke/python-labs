# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'

"""

数据抓取流程：

1. 使用帐号密码XAuth登录豆瓣，保存AccessToken，如果已经有Token，直接使用，初始化API
2. 读取种子用户ID列表，逐个取User信息写入actions数据表(只执行一次)
3. 读取actions的数据库数据，按以下流程循环：
    1. 检查action_following标志，读取followings列表，写入actions（包括ID和action_user），写入users
    2. 检查action_followers标志，读取followers列表，写入actions（包括ID和action_user），写入users
4. 读取actions的数据库数据，按以下流程循环：
    1. 检查action_user标志，读取user信息，写入actions，写入users

"""

import config
from client import ApiClient

if __name__ == "__main__":
    client = ApiClient(config.API_KEY_SHUO_ANDROID, config.API_SECRET_SHUO_ANDROID)
    if not client.token_code:
        username = raw_input("please input username:")
        password = raw_input("please input password:")
        client.auth_with_password(username, password)
        client.save_token()
    print client.token_code
    # print client.me().body
    # print client.user(1376127).body


