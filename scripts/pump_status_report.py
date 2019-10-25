#!/bin/env python3
import time
import subprocess
import requests
from config import WX_MSG_URL, STATUS_API_URL

def uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            return float(f.readline().split()[0])
    except:
        return 0


def get_status_text():
    ut = subprocess.check_output(['uptime']).decode('utf8')
    ut=f'Uptime={ut}'
    # headers = {'Accept': 'application/json'}
    r = requests.get(STATUS_API_URL)
    rs = r.text.split('\n')
    # rs.append(ut)
    return '  \n'.join(rs)


def send_wx_message(msg):
    # time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    time_str = time.strftime("%H%M%S", time.localtime())
    data = {'text': f'Pump_Status_Report_{time_str}',
            'desp': msg}
    r = requests.post(WX_MSG_URL, data=data)
    print(r.text)


if __name__ == "__main__":
    send_wx_message(get_status_text())
