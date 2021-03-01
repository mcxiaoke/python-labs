#!/usr/bin/env python
import json
import time
import requests
import bottle
import logging
from datetime import datetime
from config import WX_WORK_CORP_ID, WX_WORK_APP_ID, WX_WORK_SECRET

logger = logging.getLogger('wechat-work')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s::%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

ACCESS_TOKEN_URL = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'

SEND_MSG_URL = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'

TOKEN_EXPIRES = 7200

TOKEN_FILE = '/tmp/{}_token.json'.format(WX_WORK_CORP_ID)

_token = None
_token_ts = 0


def _load_token():
    global _token
    global _token_ts
    try:
        data = json.load(open(TOKEN_FILE, 'r'))
        if time.time()-data['ts'] < TOKEN_EXPIRES:
            _token_ts = data['ts']
            _token = data['tk']
            logger.info('token file loaded, token:%s', _token)
    except Exception:
        logger.exception('token file not found')


def _save_token(new_token):
    global _token_ts
    global _token
    if new_token and len(new_token) > 32:
        _token_ts = time.time()
        _token = new_token
        data = {
            'ts': _token_ts,
            'tk': _token
        }
        json.dump(data, open(TOKEN_FILE, 'w'))
        logger.info('token file saved, token:%s', _token)


def _send_token_request():
    token_url = ACCESS_TOKEN_URL.format(WX_WORK_CORP_ID, WX_WORK_SECRET)
    try:
        r = requests.get(token_url)
        if r.status_code == 200:
            rj = r.json()
            if rj['errcode'] == 0:
                _save_token(rj['access_token'])
            logger.info('_send_token_request, res:%s', rj)
    except Exception:
        logger.exception('_send_token_request')


def _get_token():
    if not _token or time.time() - _token_ts > TOKEN_EXPIRES:
        _send_token_request()
    return _token


def send_message(content):
    tk = _get_token()
    send_url = SEND_MSG_URL.format(tk)
    data = {
        'touser': '@all',
        'msgtype': 'text',
        'agentid': WX_WORK_APP_ID,
        'text': {
            'content': content
        }
    }
    post_json = json.dumps(data)
    try:
        r = requests.post(send_url, data=post_json)
        logger.info('send_message:[%s] response:%d %s',
                    content, r.status_code, r.json())
    except:
        logger.exception('send_message')


def main():
    _load_token()
    send_message('python 3 script, send at ' +
                 datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))



@bottle.route('/send/<corpid>')
def index(corpid):
    if corpid == WX_WORK_CORP_ID:
        return bottle.template('<b>Hello {{name}}</b>!', corpid=corpid)

bottle.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
