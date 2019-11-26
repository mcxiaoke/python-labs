from datetime import datetime
import os
import time
import logging
import requests
import socket
import struct
import re
import platform
from datetime import datetime
import time
from datetime import datetime
import paho.mqtt.client as mqtt
from config import *

logging.basicConfig(level=logging.INFO)

HOSTNAME = socket.gethostname()
THE_TOPIC = HOSTNAME+"/#"
STATUC_TOPIC = HOSTNAME+"/status"
CMD_TOPIC = HOSTNAME+"/cmd"
DCHECK_TOPIC = "device/check"
DONLINE_TOPIC = "device/online"

first_connect = True
uname = ' '.join(platform.uname())
boot = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def led_set(on_or_off):
    try:
        import gpio_led
        gpio_led.led_set(on_or_off)
    except:
        print('No LED found')
        pass


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def send_online_report():
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip = get_ip()
    data = {'text': '{}_Online_{}'.format(HOSTNAME, ip),
            'desp': 'Host: {}  \nIP: {}  \nBoot:{}  \nDate: {}'.format(uname, ip, boot, dt)}
    try:
        r = requests.post(WX_URL, data=data, timeout=10)
        logging.info(r.text[:64])
    except Exception as e:
        logging.error(e)


def publish_online():
    client.publish(STATUC_TOPIC, "Online", retain=True)


def publish_status(to_topic):
    ip = get_ip()
    client.publish(
        to_topic, "{}/{} Boot: {} Info: {}".format(HOSTNAME, ip, boot, uname))


def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode('utf8')
    logging.info(topic+" - "+message.replace("\n", " ") +
                 " ("+str(msg.qos)+","+str(msg.retain)+")")
    cmd_list = ('check', 'status', '?')
    if topic == DCHECK_TOPIC:
        publish_status(DONLINE_TOPIC)
    elif topic == CMD_TOPIC and message in cmd_list:
        publish_status(STATUC_TOPIC)


def on_connect(client, userdata, flags, rc):
    logging.info("MQTT Connected with result: "+mqtt.error_string(rc))
    # client.subscribe("$SYS/#")
    client.subscribe(CMD_TOPIC)
    client.subscribe(DCHECK_TOPIC)
    publish_online()
    publish_status(STATUC_TOPIC)
    publish_status(DONLINE_TOPIC)
    global first_connect
    if first_connect:
        send_online_report()
        first_connect = False
    led_set(True)


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result: "+mqtt.error_string(rc))
    led_set(False)


def create_client():
    client = mqtt.Client(clean_session=True)
    # client.enable_logging()
    # client.on_log = on_log
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.will_set(STATUC_TOPIC, payload="Offline", retain=True)
    client.connect(MQTT_SERVER, port=MQTT_PORT, keepalive=15)
    return client


if __name__ == "__main__":
    client = create_client()
    logging.info("{} device status monitor online".format(HOSTNAME))
    client.loop_forever()
