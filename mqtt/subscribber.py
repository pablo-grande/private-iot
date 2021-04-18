#!/usr/bin/env python3
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from config import gateway_config


SERVER, PORT = gateway_config['server'], gateway_config['port']
topic = '#'


def on_connect(client, userdata, flags, rc):
    print(f'connected to {SERVER}:{PORT} with result code {rc}')
    # subscribing here will mean renewed subscription after losing connection
    print(f'About to subscribe to {topic}')
    client.subscribe(topic)


def on_message(client, userdata, message):
    print(f"{SERVER}/{message.topic}/p={message.payload} (QoS={message.qos})")


client = mqtt.Client('subscribber', transport='tcp')
client.on_connect = on_connect
client.on_message = on_message
client.connect(SERVER, PORT)
client.loop_forever()

