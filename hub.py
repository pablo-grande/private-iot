#!/usr/bin/env python
# -*- coding: utf-8 -*
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads
from os import getenv
from sys import argv
from requests import session

from matrix_client.client import MatrixClient
from matrix_client.errors import MatrixHttpLibError

from settings import (
    ONION_ADDR,
    LOGGER
)


logging.basicConfig(level=logging.INFO)


class HiddenService:
    session = session()
    proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050'
    }

    def __init__(self, *args, **kwargs):
        self.session.proxies = self.proxies
        self.addrs = ONION_ADDR

    def put(self, id_device, data):
        self.url = f"http://{self.addrs[id_device]}"
        json_data = {'id_device': id_device, 'data': data}
        session_obj = self.session.put(self.url, json=json_data)
        if session_obj.ok:
            logging.debug(json_data)
        else:
            logging.error(f"failed to connect {self.url}")


class Logger:
    address: str
    port: int
    token: str
    room: dict

    def __init__(self, *args, **kwargs):
        self.address, self.port = args[0]
        _room_name = args[1]
        _room = LOGGER[_room_name]
        if 'username' not in kwargs:
            kwargs.update({'username': _room["user"]})
        if 'password' not in kwargs:
            kwargs.update({'password': _room["password"]})
        try:
            # TODO: Make also dynamic
            self._client = MatrixClient(f"http://localhost:8008")
            self.token = self._client.login(**kwargs)
            self.room = self._client.join_room(_room_name)
        except MatrixHttpLibError as matrix_error:
            logging.error(matrix_error)

    def log(self,  message):
        # TODO: Allow reconnection with room name as param
        if not self.token:
            logging.error(f"MatrixClient was not properly intialized. No log can be done")
            return
        logging.info(f"Sending {message} to {self.room}")
        self.room.send_text(message)


class ProxyHandler(BaseHTTPRequestHandler):
    logger: Logger
    hidden_service: HiddenService

    def __init__(self, *args, **kwargs):
        # FIXME
        room_name = list(LOGGER.keys())[0]
        self.logger = Logger(args[1], room_name)
        self.hidden_service = HiddenService(ONION_ADDR)
        super().__init__(*args, **kwargs)

    def _send_response(self, code=200):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"")

    def do_PUT(self):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length).decode("utf-8")
        logging.info(
            f"PUT request was:\n\
            Path: {self.path}\n\
            Headers: {self.headers}\
            Body: {put_data}"
        )
        device_data = loads(put_data)
        id_device = device_data["device"]
        to_send = f"{device_data['topic']}: {device_data['payload']}"
        self.hidden_service.put(id_device, to_send)
        self.logger.log(to_send)
        self._send_response()

    def do_GET(self):
        content_length = int(self.headers["Content-Length"])
        self._send_response()

    def send_error(self, *args, **kwargs):
        self._send_response(400)


def run(server_class=HTTPServer, handler_class=ProxyHandler, port=8000):
    httpd = server_class(("", port), handler_class)
    try: httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server execution")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    print("Starting server execution")
    if len(argv) > 1:
        port = int(argv[1])
        run(port=int(port))
    else:
        run()
