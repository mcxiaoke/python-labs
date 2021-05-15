'''
File: lan_monitor.py
Created: 2021-05-15 16:24:29
Modified: 2021-05-15 16:25:12
Author: mcxiaoke (github@mcxiaoke.com)
License: Apache License 2.0
'''

import socket
import threading
import traceback
import time
import datetime
import requests
import pprint
from config import WX_REPORT_URL

DEVICES = [
    ("Mini", "Xiaomi Mini OpenWrt", "192.168.1.2", 22),
    ("OneCloud", "One Cloud OpenWrt", "192.168.1.3", 22),
    ("DF975D", "ESP Watering Device", "192.168.1.116", 80),
    ("N1BOX", "N1 Armbian Server", "192.168.1.114", 22),
    ("HP400G1", "HP400 x86 Server", "192.168.1.118", 22)]

status = {}


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def send_message(dv):
    name, desc, ip, port = dv
    title = "Device {} {}".format(
        name, ('Online' if status.get(ip) else 'Offline'))
    desp = "IP: {} ({})".format(ip, desc)
    data = {'title': title, "desp": desp}
    online = "Online" if status.get(ip) else "Offline"
    try:
        r = requests.get(WX_REPORT_URL, data=data)
        # print(r.status_code, r.text)
        print('{} {} send ok.'.format(dv, online))
    except Exception as e:
        print('{} {} send failed: {}'.format(dv, online, e))


def check_port_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        ret = s.connect_ex((ip, port))
        return ret == 0
    except OSError as e:
        # print('{} failed: {}'.format(ip, e))
        return False
    finally:
        s.close()


def check_device(dv):
    name, desc, ip, port = dv
    old_st = status.get(ip)
    new_st = check_port_open(ip, port)
    if old_st != new_st:
        status[ip] = new_st
        # st = ('online' if new_st else 'offline')
        # print('{} status changed to {}'.format(ip, st))
        send_message(dv)
    else:
        # print('Not Changed: {}'.format(ip))
        pass


def check_all():
    threading.Timer(60, check_all).start()
    print("Checking at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for dv in DEVICES:
        check_device(dv)
        time.sleep(2)


if __name__ == '__main__':
    me = ("Lan Monitor", "Lan Device Monitor", get_ip(), 22)
    socket.setdefaulttimeout(3)
    check_all()
    check_device(me)
