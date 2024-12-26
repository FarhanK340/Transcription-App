from django.test import TestCase
from django.urls import reverse
from chatApp.models import Room, Message

class TestChatAppCreateRoomView(TestCase):
    def setUp(self):
        # Create a sample room and message for testing
        self.room = Room.objects.create(room_name="test_room")
        self.message = Message.objects.create(
            room=self.room,
            sender="test_user",
            message="Hello, World!"
        )

    # test create room view with post request for a new room
    def test_create_room_new_room(self):
        """Test creating a new room via the CreateRoom view."""
        response = self.client.post(reverse('chatApp:create-room'), {
            'username': 'test_user',
            'room': 'new_room'
        })

        # Check if the room is created
        self.assertTrue(Room.objects.filter(room_name='new_room').exists())
        # Check if redirected to the correct room
        self.assertRedirects(response, reverse('chatApp:room', kwargs={
            'room_name': 'new_room',
            'username': 'test_user'
        }))


    # test create room view with post request for an existing room
    def test_create_room_existing_room(self):
        """Test redirecting to an existing room via the CreateRoom view."""
        response = self.client.post(reverse('chatApp:create-room'), {
            'username': 'test_user',
            'room': 'test_room'
        })

        # Ensure no duplicate room is created
        self.assertEqual(Room.objects.filter(room_name='test_room').count(), 1)
        # Check if redirected to the correct room
        self.assertRedirects(response, reverse('chatApp:room', kwargs={
            'room_name': 'test_room',
            'username': 'test_user'
        }))

    # test create room view with get request
    def test_create_room_get_request(self):
        """Test the behavior of the CreateRoom view with a GET request."""
        response = self.client.get(reverse('chatApp:create-room'))

        # Check if the response status is OK
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'chatApp/index.html')


class TestChatAppMessageView(TestCase):
    def setUp(self):
        # Create a sample room and message for testing
        self.room = Room.objects.create(room_name="test_room")
        self.message = Message.objects.create(
            room=self.room,
            sender="test_user",
            message="Hello, World!"
        )

    def test_message_view_valid_room(self):
        """Test retrieving messages for a valid room."""
        response = self.client.get(reverse('chatApp:room', kwargs={
            'room_name': 'test_room',
            'username': 'test_user'
        }))

        # Check if the response status is OK
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'chatApp/message.html')
        # Check if the context data is correct
        self.assertIn('messages', response.context)
        self.assertIn('user', response.context)
        self.assertIn('room_name', response.context)
        self.assertEqual(response.context['user'], 'test_user')
        self.assertEqual(response.context['room_name'], 'test_room')
        self.assertQuerysetEqual(
            response.context['messages'],
            Message.objects.filter(room=self.room),
            transform=lambda x: x
        )

    def test_message_view_invalid_room(self):
        """Test the behavior when the room does not exist."""
        response = self.client.get(reverse('chatApp:room', kwargs={
            'room_name': 'invalid_room',
            'username': 'test_user'
        }))

        # Check if the response status code is 404
        self.assertEqual(response.status_code, 404)


    # check the message view for a room with no messages
    def test_message_view_no_messages(self):
        """Test the behavior when the room has no messages."""
        # Create a new room without messages
        new_room_with_no_messages = Room.objects.create(room_name="new_room_with_no_messages")

        response = self.client.get(reverse('chatApp:room', kwargs={
            'room_name': 'new_room_with_no_messages',
            'username': 'test_user'
        }))

        # Check if the response status is OK
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'chatApp/message.html')
        # Check if the context data is correct
        self.assertIn('messages', response.context)
        self.assertIn('user', response.context)
        self.assertIn('room_name', response.context)
        self.assertEqual(response.context['user'], 'test_user')
        self.assertEqual(response.context['room_name'], 'new_room_with_no_messages')
        self.assertQuerysetEqual(
            response.context['messages'],
            Message.objects.filter(room=new_room_with_no_messages),
            transform=lambda x: x
        )
