from matrix_client.client import MatrixClient
from ipdb import set_trace

client = MatrixClient("http://localhost:8008")

set_trace()

# New user
# token = client.register_with_password(username="pacemaker", password="MDTweSomWY")

# Existing user
token = client.login(username="pacemaker", password="MDTweSomWY")

room = client.join_room("cardio")
room.send_text("Hello!")

