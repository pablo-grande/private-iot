#!/usr/bin/env python
# -*- coding: utf-8 -*
import paho.mqtt.client as mqtt
from config import commissioner_config as config
from time import sleep
from random import choice


SERVER, PORT = config['server'], config['port']
username, password = config['username'], config['password']

def on_connect(client, userdata, flags, rc):
    if not rc:
        print("connected to server")
        global connected
        connected = True
    else:
        print("something went wrong")


connected = False

client = mqtt.Client('publisher', transport='websockets')
client.on_connect = on_connect
client.username_pw_set(username=username, password=password)
client.connect(SERVER, PORT)
client.loop_start()

while not connected:
    print("not connected")
    sleep(0.1)  # wait for it...

try:
    while True:
        topic, payload = "CaSesLlucies/GW/C2S", "00007f0111"
        print(f'About to publish on {topic} payload: {payload}')
        res = client.publish(topic, payload)
        sleep(0.4)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()

