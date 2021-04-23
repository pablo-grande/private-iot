import requests

session = requests.session()
session.proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

URL = "http://xwjtp3mj427zdp4tljiiivg2l5ijfvmt5lcsfaygtpp6cw254kykvpyd.onion"
session_obj = session.put(URL, json={'data': 500})
from ipdb import set_trace
set_trace()
