import logging
import time
import paho.mqtt.client as mqtt
from config import *


logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s][%(levelname)s] %(message)s',
                        datefmt='%m%d_%H%M%S')
logger = logging.getLogger("mqtt")

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result: " + mqtt.error_string(rc))
    # client.subscribe("$SYS/#")
    # client.subscribe("device/#")

def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode('utf8')
    logMsg = "[{}]:<{}> ({},{})".format(topic, message, msg.qos, msg.retain)
    logger.info(logMsg)

def create_client():
    client = mqtt.Client(client_id='mqtt-publish-test-a', clean_session=False)
    # client.enable_logger()
    # client.on_log = on_log
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(MQTT_SERVER, port=MQTT_PORT, keepalive=60)
    return client

def send_message(topic,message):
    client = create_client()
    client.loop_start()
    time.sleep(2)
    ret = client.publish(topic, message)
    logger.info('Send message result: {}:{}/{}'.format(topic,message,ret))
    client.loop_write()
    # client.loop_read()
    client.loop_stop()
    client.disconnect()
    return ret




if __name__ == "__main__":
    send_message('device/test','hello world, publish test!')