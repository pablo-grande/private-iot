#!/usr/bin/env python3
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from config import gateway_config
from requests import put


SERVER, PORT = gateway_config['server'], gateway_config['port']
topic = '#'


def on_connect(client, userdata, flags, rc):
    print(f'connected to {SERVER}:{PORT} with result code {rc}')
    # subscribing here will mean renewed subscription after losing connection
    print(f'About to subscribe to {topic}')
    client.subscribe(topic)


def on_message(client, userdata, message):
    # TODO: Change payload from Arduino itself
    payload = message.payload.decode('utf-8').split(":")[-1].strip()
    print(f"{SERVER}/{message.topic}/p={payload} (QoS={message.qos})")
    topic = message.topic.split("/")[-1]
    # send message to hub
    # TODO: incorporate message broker into hub itself
    put("http://localhost:8000", json={"device": "patient", "topic": topic, "payload": payload})



client = mqtt.Client('subscribber', transport='tcp')
client.on_connect = on_connect
client.on_message = on_message
client.connect(SERVER, PORT)
client.loop_forever()
