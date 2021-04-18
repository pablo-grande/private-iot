from ipdb import set_trace
from matrix_client.client import MatrixClient

client = MatrixClient("http://localhost:80")

# New user
# token = client.register_with_password(username="someother_name", password="kark6424")

# Existing user
set_trace()
token = client.login(username="virgil", password="kark6424")

room = client.join_room("#test_unsecure_2:localhost")
room.send_text("Hello!")

