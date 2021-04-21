import requests

session = requests.session()
session.proxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

session_obj = session.get("http://onionshare:gentleman-nurture@v5eiiowe25r6ukd7dofpvkksix3v25mmyuiaqtunz53sjaciy2juatyd.onion")
from ipdb import set_trace
set_trace()
print(session_obj.headers)

