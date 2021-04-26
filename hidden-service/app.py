import logging
import redis

from datetime import datetime
from time import sleep

from flask import Flask, request

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


@app.route('/', methods=['PUT', 'GET'])
def register():
    if request.method == "GET":
        heartbeat_data = sorted([ 
            f"{key.decode('utf-8')}: {cache.get(key).decode('utf-8')}"
            for key in cache.scan_iter("data:*")
        ])
        return f"<ul><li>{'</li><li>'.join(heartbeat_data)}</ul>"

    retries = 5
    post_request = request.json
    logging.debug(post_request)
    while True:
        try:
            logging.debug("Trying to save data")
            cache.set(
                f"data:{datetime.now()}",
                post_request["data"]
            )
            return '', 200
        except redis.exceptions.ConnectionError as exc:
            logging.info("Redis exception, retry")
            if retries == 0:
                raise exc
            retries -= 1
            sleep(0.5)
