#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-04 22:45:54

from xauth import AuthClient
from xauth import test_get_access_token
import config
import requests
import oauthlib
from requests_oauthlib import OAuth1
from urlparse import parse_qs


def get_token():
    oauth = OAuth1(config.CONSUMER_KEY, client_secret=config.CONSUMER_SECRET)
    r = requests.post(url=config.TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    print credentials

# http://requests-oauthlib.readthedocs.org/en/latest/oauth1_workflow.html
# https://github.com/FanfouAPI/FanFouAPIDoc/wiki/Apicategory

if __name__ == '__main__':
    client = AuthClient(
        config.CONSUMER_KEY, config.CONSUMER_SECRET, config.TOKEN_URL)
    access_token = client.get_access_token(config.USERNAME, config.PASSWORD)
    print access_token

    oauth = OAuth1(config.CONSUMER_KEY,
                   client_secret=config.CONSUMER_SECRET,
                   resource_owner_key=access_token["oauth_token"],
                   resource_owner_secret=access_token["oauth_token_secret"],
                   signature_type='auth_header')
    verify_url = config.API_HOST+config.VERIFY
    r = requests.get(url=verify_url, auth=oauth)
    print r.status_code, r.text
    # get_token()
