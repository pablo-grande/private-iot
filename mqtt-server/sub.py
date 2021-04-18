#!/usr/bin/env python
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from config import gateway_config as gateway_config
from requests import post
from ssl import PROTOCOL_TLS


SERVER, PORT = gateway_config['server'], gateway_config['port']
username, password = gateway_config['username'], gateway_config['password']
topic = '#'


def on_connect(client, userdata, flags, rc):
    print(f'connected to {SERVER}:{PORT} with result code {rc}')
    # subscribing here will mean renewed subscription after losing connection
    print(f'About to subscribe to {topic}')
    client.publish("testing", "missatge_test")
    client.subscribe(topic)


def on_message(client, userdata, message):
    print(f"{SERVER}/{message.topic}/p={message.payload} (QoS={message.qos})")


client = mqtt.Client('subscribber', transport='tcp')
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=None,
    tls_version=PROTOCOL_TLS, ciphers=None)
client.username_pw_set(username=username, password=password)
client.connect(SERVER, PORT)
client.loop_forever()

