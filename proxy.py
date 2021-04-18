#!/usr/bin/env python
# -*- coding: utf-8 -*
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads
from logging import basicConfig, INFO, info as log
from os import getenv
from sys import argv

from matrix_client.client import MatrixClient

basicConfig(level=INFO)

LOG_USER = getenv('LOG_USER')
LOG_PASSWORD = getenv('LOG_PASSWORD')
LOG_ROOM = getenv('LOG_ROOM')


# TODO:
# class ProxyHandler(BasteHTTPRequestHandler, MatrixClient)
class ProxyHandler(BaseHTTPRequestHandler):

    def _send_response(self, code=200):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"")

    def do_PUT(self):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length).decode("utf-8")
        log(
            f"PUT request was:\n\
            Path: {self.path}\n\
            Headers: {self.headers}\
            Body: {put_data}"
        )
        device_data = loads(put_data)
        id_device = device_data["device_id"]
        to_send = device_data["data"]

        # send data to .onion service

        # log
        client = MatrixClient(getenv(LOGGING_SERVER, "http://localhost:80")
        token = client.login(username=LOG_USER, password=LOG_PASSWORD)
        room = client.create_room("test_unsecure_2")
        room.send_text("Hello!")
        self._send_response()

    def do_GET(self):
        content_length = int(self.headers["Content-Length"])
        self._send_response()

    def send_error(self, *args, **kwargs):
        self._send_response(400)


def run(server_class=HTTPServer, handler_class=ServerHandler, port=8000):
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
