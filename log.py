#!/usr/bin/env python
# -*- coding: utf-8 -*
from requests import post
from os import getenv
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

LOGGING_ENDPOINT = "http://localhost:80"

username = getenv("LOGGER_USER")
password = getenv("LOGGER_PASSWORD")

response = get()
if response.ok:
    logging.info("Notify data send")
    send = post()
    if not send.ok:
        logging.error("Data could not be sent")
