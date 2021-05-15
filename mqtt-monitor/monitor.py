#!/usr/bin/env python3

from datetime import datetime
import logging
import requests
import threading
import re
import time
import paho.mqtt.client as mqtt
from config import *

MSG_LIMIT_PER_MIN = 60
MSG_LIMIT_PER_HOUR = 300
MSG_LIMIT_PER_DAY = 1500

sendCounter = {}
titleCounter = 0

IP = '127.0.0.1'

def get_public_ip():
    global IP
    try:
        json = requests.get('http://ip-api.com/json').json()
        IP =  json['query']
        logger.info('Public IP:', IP)
    except Exception as e:
        logger.error(e)

def get_full_class_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__


def get_log_filename():
    dt = datetime.now().strftime("%Y%m%d")
    return '/tmp/mqtt-monitor-{}.log'.format(dt)


def logging_config():
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s][%(levelname)s] %(message)s',
                        datefmt='%m%d_%H%M%S',
                        filename=get_log_filename(),
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


logging_config()
logger = logging.getLogger("monitor")


def send_ios_report(data):
    try:
        url = BARK_REPORT_URL.format(data['title'], data['desp'])
        r = requests.post(url, timeout=10)
        if r.ok:
            logger.debug("iOS sent: %s", data["title"])
        else:
            logger.warning("iOS send for %s failed, error: %s %s",
                           sender, r.status_code, r.text)
    except Exception:
        logger.exception('ios send failed')


def send_report(sender, msg):
    global sendCounter
    global titleCounter
    now = datetime.now()
    min_key = now.strftime("Min:%Y-%m-%d %H:%M")
    day_key = now.strftime("Day:%Y-%m-%d")
    min_value = sendCounter.get(min_key, 0)
    day_value = sendCounter.get(day_key, 0)
    if min_value > MSG_LIMIT_PER_MIN:
        logger.warning(
            'Report exceed limits: {} = {}'.format(min_key, min_value))
        return
    if day_value > MSG_LIMIT_PER_DAY:
        logger.warning(
            'Report exceed limits: {} = {}'.format(day_key, day_value))
        return
    sendCounter[min_key] = min_value + 1
    sendCounter[day_key] = day_value + 1
    titleCounter += 1
    data = {
        "title": "Device_{}_Message_{}".format(sender, titleCounter),
        "desp": msg,
    }
    try:
        r = requests.post(WX_REPORT_URL, params=data, timeout=10)
        if r.ok:
            logger.info("Sent: [%s]", data["title"])
            logger.debug("Send report for %s successful", sender)
        else:
            logger.warning("Send report for %s failed, error: %s %s",
                           sender, r.status_code, r.text)
    except Exception:
        logger.exception('send report failed')
    time.sleep(1)
    send_ios_report(data)

def send_online():
    time.sleep(1)
    logger.info('Send monitor online')
    client.publish("device/online", "MQTT Monitor/Online {}".format(IP), retain=True)
    send_report("monitor", "MQTT Monitor/Online {}".format(IP))
    
def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode('utf8')
    logMsg = "[{}]:<{}> ({},{})".format(topic, message, msg.qos, msg.retain)
    logger.info(logMsg)
    if topic == 'device/monitor/status':
        return
    if topic == 'device/check':
        t = threading.Thread(target=send_online)
        t.start()
        return
    m = re.match(r"^device/(\S+)/status$", topic)
    if m and m.group(1):
        t = threading.Thread(target=send_report, args= (m.group(1), message,))
        t.start()
#         send_report(m.group(1), message)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result: " + mqtt.error_string(rc))
    # client.subscribe("$SYS/#")
    client.subscribe("device/#")
    _thread.start_new_thread(send_online)

def on_disconnect(client, userdata, rc):
    logger.info("Disconnected with result: " + mqtt.error_string(rc))


def create_client():
    client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=False)
    # client.enable_logger()
    # client.on_log = on_log
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.will_set("device/online", payload="MQTT Monitor/Offline {}".format(IP), retain=True)
    client.connect(MQTT_SERVER, port=MQTT_PORT, keepalive=60)
    return client


if __name__ == "__main__":
    get_public_ip()
    client = create_client()
    logger.info("====================")
    logger.info("MQTT Monitor Started")
    client.loop_forever()
