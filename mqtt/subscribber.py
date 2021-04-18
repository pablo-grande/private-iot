#!/usr/bin/env python3
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from config import gateway_config
from matrix_client.client import MatrixClient


SERVER, PORT = gateway_config['server'], gateway_config['port']
matrix_username, matrix_password = gateway_config['m_user'], gateway_config['m_pass']
topic = '#'


def on_connect(client, userdata, flags, rc):
    print(f'connected to {SERVER}:{PORT} with result code {rc}')
    # subscribing here will mean renewed subscription after losing connection
    print(f'About to subscribe to {topic}')
    client.subscribe(topic)


def on_message(client, userdata, message):
    print(f"{SERVER}/{message.topic}/p={message.payload} (QoS={message.qos})")
    room = matrix_client.join_room("pacemaker")
    room.send_text("A message was sent to your doctor today!")


matrix_client = MatrixClient("http://localhost:80")
token = matrix_client.login(username=matrix_username, password=matrix_password)
client = mqtt.Client('subscribber', transport='tcp')
client.on_connect = on_connect
client.on_message = on_message
client.connect(SERVER, PORT)
client.loop_forever()




# New user
# token = client.register_with_password(username="someother_name", password="kark6424")

# Existing user
set_trace()


