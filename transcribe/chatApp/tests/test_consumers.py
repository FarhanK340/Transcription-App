# import pytest
# import json
# from channels.testing import WebsocketCommunicator
# from asgiref.testing import ApplicationCommunicator
# from channels.layers import get_channel_layer
# from chatApp.consumers import ChatConsumer
# from chatApp.models import Room, Message


# @pytest.mark.asyncio
# class TestChatConsumer:
#     @pytest.fixture
#     async def setup(self, db):
#         """Set up a test room and return room name."""
#         room = Room.objects.create(room_name="test_room")
#         return room.room_name

#     async def communicator(self, setup):
#         """Create a WebSocket communicator for the test room."""
#         room_name = setup
#         communicator = WebsocketCommunicator(ChatConsumer, f"/ws/chat/{room_name}/")
#         connected, _ = await communicator.connect()
#         assert connected
#         yield communicator
#         await communicator.disconnect()

#     # async def test_connect(self, communicator):
#     #     """Test if WebSocket connection is successfully established."""
#     #     assert communicator  # Connection established in fixture

#     # async def test_disconnect(self, setup):
#     #     """Test if WebSocket connection is successfully disconnected."""
#     #     room_name = setup
#     #     communicator = WebsocketCommunicator(ChatConsumer, f"/ws/chat/{room_name}/")

#     #     # Connect the WebSocket
#     #     connected, _ = await communicator.connect()
#     #     assert connected

#     #     # Disconnect the WebSocket
#     #     await communicator.disconnect()
#     #     # If no errors occur, it disconnects cleanly
#     #     assert True

#     # async def test_send_and_receive_message(self, communicator, setup):
#     #     """Test sending and receiving a WebSocket message."""
#     #     room_name = setup
#     #     test_message = {
#     #         "room_name": room_name,
#     #         "sender": "test_user",
#     #         "message": "Hello, World!",
#     #     }

#     #     # Send the message to the WebSocket
#     #     await communicator.send_json_to(test_message)

#     #     # Receive the response
#     #     response = await communicator.receive_json_from()

#     #     # Check the structure of the response
#     #     assert response["message"]["sender"] == "test_user"
#     #     assert response["message"]["message"] == "Hello, World!"

#     # async def test_message_saved_in_db(self, communicator, setup, db):
#     #     """Test if a message is saved to the database when sent."""
#     #     room_name = setup
#     #     test_message = {
#     #         "room_name": room_name,
#     #         "sender": "test_user",
#     #         "message": "Hello, DB!",
#     #     }

#     #     # Send the message to the WebSocket
#     #     await communicator.send_json_to(test_message)

#     #     # Ensure the message is saved in the database
#     #     await communicator.receive_json_from()
#     #     saved_message = Message.objects.filter(message="Hello, DB!").first()

#     #     assert saved_message is not None
#     #     assert saved_message.room.room_name == room_name
#     #     assert saved_message.sender == "test_user"
#     #     assert saved_message.message == "Hello, DB!"

#     # async def test_group_message(self, setup):
#     #     """Test if a message sent to the group is broadcast to all group members."""
#     #     room_name = setup
#     #     channel_layer = get_channel_layer()

#     #     # Create two communicators for the same room
#     #     communicator_1 = WebsocketCommunicator(ChatConsumer, f"/ws/chat/{room_name}/")
#     #     communicator_2 = WebsocketCommunicator(ChatConsumer, f"/ws/chat/{room_name}/")

#     #     # Connect both communicators
#     #     connected_1, _ = await communicator_1.connect()
#     #     connected_2, _ = await communicator_2.connect()

#     #     assert connected_1
#     #     assert connected_2

#     #     # Send a message to the group
#     #     test_message = {
#     #         "room_name": room_name,
#     #         "sender": "test_user",
#     #         "message": "Group message",
#     #     }
#     #     await channel_layer.group_send(
#     #         f"room_{room_name}",
#     #         {
#     #             "type": "send_message",
#     #             "message": test_message,
#     #         },
#     #     )

#     #     # Receive messages from both communicators
#     #     response_1 = await communicator_1.receive_json_from()
#     #     response_2 = await communicator_2.receive_json_from()

#     #     # Check if both communicators received the message
#     #     assert response_1["message"]["message"] == "Group message"
#     #     assert response_2["message"]["message"] == "Group message"

#     #     # Disconnect both communicators
#     #     await communicator_1.disconnect()
#     #     await communicator_2.disconnect()
