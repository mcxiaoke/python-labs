#!/usr/bin/env python3
# encoding: utf-8
import time
from datetime import datetime
from typing import Mapping
import requests
import os
import sys
from config import WX_REPORT_URL


def send_mqtt(content):
    pass


def send_message(title, desp):
    data = {'title': title, "desp": desp}
    try:
        r = requests.get(WX_REPORT_URL, data=data)
        print('send ok:', r.status_code, r.text)
    except Exception as e:
        print('send failed: {}'.format(e))


def gammu_forward():
    print('SMS_MESSAGES:{}'.format(os.getenv('SMS_MESSAGES')))
    print('DECODED_PARTS:{}'.format(os.getenv('DECODED_PARTS')))
    # print('PHONE_ID:{}'.format(os.getenv('PHONE_ID')))
    # print('SMS_1_NUMBER:{}'.format(os.getenv('SMS_1_NUMBER')))
    # print('SMS_1_TEXT:{}'.format(os.getenv('SMS_1_TEXT')))
    # print('SMS_2_NUMBER:{}'.format(os.getenv('SMS_2_NUMBER')))
    # print('SMS_2_TEXT:{}'.format(os.getenv('SMS_2_TEXT')))
    # print('DECODED_1_TEXT:{}'.format(os.getenv('DECODED_1_TEXT')))
    # print('DECODED_1_MMS_SENDER:{}'.format(os.getenv('DECODED_1_MMS_SENDER')))
    # print('DECODED_2_TEXT:{}'.format(os.getenv('DECODED_2_TEXT')))
    # print('DECODED_2_MMS_SENDER:{}'.format(os.getenv('DECODED_2_MMS_SENDER')))

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sender = os.environ['SMS_1_NUMBER']
    numParts = int(os.environ['DECODED_PARTS'])
    text = ""
    try:
        if numParts == 0:
            text = os.environ['SMS_1_TEXT']
        else:
            for i in range(1, numParts + 1):
                envName = "DECODED_%d_TEXT" % i
                if envName in os.environ:
                    text = text + os.environ[envName]
    except Exception as e:
        print("forward {} sms error {}", sender, e)
    title = "来自{}的短信".format(sender)
    desp = "\n{} ({})".format(text, now)
    # desp = "\n内容：{}\n来自：{}\n时间：{}".format(text, sender, now)
    print('forward sms for [{}]'.format(sender))
    send_message(title, desp)


if __name__ == '__main__':
    gammu_forward()
