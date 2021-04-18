#!/usr/bin/env python
# -*- coding: utf-8 -*
from paho.mqtt.client import Client
from config import commissioner_config, gateway_config
from ssl import PROTOCOL_TLS


messages = []

def on_message(client, userdata, message):
    print(f"{client._host}:{client._port}/{message.topic}/p={message.payload} (QoS={message.qos})")
    messages.append((message.topic, message.payload))


def on_connect(client, userdata, flags, rc):
    if not rc:
        print(f"connected to {client._host}:{client._port}")
        client.subscribe('#')
    else:
        print("something went wrong")


commissioner_client = Client('commissioner-client', transport='websockets')
commissioner_client.on_connect = on_connect
commissioner_client.on_message = on_message
commissioner_client.connect(commissioner_config['server'], commissioner_config['port'])
commissioner_client.loop_start()

gw_publisher = Client('gw-publisher', transport='tcp')
gw_publisher.on_connect = on_connect
gw_publisher.username_pw_set(gateway_config['username'], gateway_config['password'])
gw_publisher.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=None,
    tls_version=PROTOCOL_TLS, ciphers=None)
gw_publisher.connect(gateway_config['server'], gateway_config['port'])
gw_publisher.loop_start()

try:
    while True:
        if messages:
            topic, payload = messages.pop()
            print(f'About to publish on {topic} payload: {payload}')
            res = gw_publisher.publish(topic, payload)

except KeyboardInterrupt:
    commissioner_client.disconnect()
    commissioner_client.loop_stop()
    gw_publisher.disconnect()
    gw_publisher.loop_stop()

