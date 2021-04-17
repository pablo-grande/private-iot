from matrix_client.client import MatrixClient

client = MatrixClient("http://localhost:80")

# New user
token = client.register_with_password(username="foobar", password="monkey")

# Existing user
token = client.login(username="foobar", password="monkey")

room = client.create_room("my_room_alias")
room.send_text("Hello!")
