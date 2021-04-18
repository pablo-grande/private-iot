#!/usr/bin/env python
# -*- coding: utf-8 -*

commissioner_config = {
    'server': '127.0.0.1',
    'port': 9001,
    'username': 'tctmqtt',
    'password': 'ansonlab',
}

gateway_config = commissioner_config.copy()
gateway_config['port'] = 8883
gateway_config['server'] = 'llamp.conectabalear.net'
