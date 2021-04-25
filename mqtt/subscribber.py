#!/usr/bin/env python3
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from config import gateway_config
from matrix_client.client import MatrixClient
from requests import put


SERVER, PORT = gateway_config['server'], gateway_config['port']
matrix_username, matrix_password = gateway_config['m_user'], gateway_config['m_pass']
topic = '#'

messages = []


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
    room.send_text(f"This is what's sent to your doctor: {payload}")
    # send message to hub
    # TODO: incorporate message broker into hub itself
    put("http://localhost:8000", json={"device": "patient", "topic": topic, "payload": payload})



matrix_client = MatrixClient("http://localhost:8008")
token = matrix_client.login(username=matrix_username, password=matrix_password)
room = matrix_client.join_room("!qKGqWURPTdcyFQHFjJ:casper.magi.sys")
client = mqtt.Client('subscribber', transport='tcp')
client.on_connect = on_connect
client.on_message = on_message
client.connect(SERVER, PORT)
client.loop_forever()




# New user
# token = client.register_with_password(username="someother_name", password="kark6424")

# Existing user
set_trace()


