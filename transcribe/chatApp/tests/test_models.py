from django.test import TestCase
from django.core.exceptions import ValidationError

from chatApp.models import Room, Message

class RoomModelTest(TestCase):
    # validate max_length constraints
    def test_room_name_max_length(self):
        room = Room.objects.create(room_name='a'*255)
        self.assertEqual(room.room_name, 'a'*255)

    # check that Room is created with a name of length 1
    def test_room_name_min_length(self):
        room = Room.objects.create(room_name='a')
        self.assertEqual(room.room_name, 'a')

    # check that Room is not created with a null name
    def test_room_name_empty(self):
        with self.assertRaises(Exception):
            Room.objects.create(room_name=None)

    # check that Room is not created with an empty name
    def test_room_name_empty(self):
        room = Room(room_name='')
        with self.assertRaises(ValidationError):
            room.full_clean()  # Explicitly validate the model

    # check that Room is not created with a name of length 256
    def test_room_name_max_length_plus_one(self):
        room = Room(room_name='a'*256)
        with self.assertRaises(ValidationError):
            room.full_clean()  # Explicitly validate the model

    # check that Room is created with a unique name
    def test_room_name_unique(self):
        room1 = Room.objects.create(room_name='room1')
        room2 = Room.objects.create(room_name='room2')
        self.assertEqual(room1.room_name, 'room1')
        self.assertEqual(room2.room_name, 'room2')

    # check that Room is created with a name of length 10
    def test_room_name_length_10(self):
        room = Room.objects.create(room_name='a'*10)
        self.assertEqual(room.room_name, 'a'*10)

    # check that Room is not created with a duplicate name
    def test_room_name_unique(self):
        room1 = Room.objects.create(room_name='room1')
        with self.assertRaises(Exception):
            Room.objects.create(room_name='room1')

    # Validate __str__ method
    def test_room_name_str(self):
        room = Room.objects.create(room_name='room1')
        self.assertEqual(room.__str__(), 'room1')

    # verify created_at and timestamp fields are auto populated
    def test_created_at_auto_populated(self):
        room = Room.objects.create(room_name='room1')
        self.assertIsNotNone(room.created_at)


class MessageModelTest(TestCase):
    # check that message is created with a sender of length 255
    def test_sender_max_length(self):
        room = Room.objects.create(room_name='a'*255)
        message = Message.objects.create(room=room, sender='a'*255, message='Hello')
        self.assertEqual(message.sender, 'a'*255)

    #check that message is created with a sender of length 1
    def test_sender_min_length(self):
        room = Room.objects.create(room_name='room1')
        message = Message.objects.create(room=room, sender='a', message='Hello')
        self.assertEqual(message.sender, 'a')

    # check that message is not created with a null sender
    def test_sender_empty(self):
        room = Room.objects.create(room_name='room1')
        with self.assertRaises(Exception):
            Message.objects.create(room=room, sender=None, message='Hello')

    # check that messsage is not created with a sender of length 10
    def test_sender_length_10(self):
        room = Room.objects.create(room_name='room1')
        message = Message.objects.create(room=room, sender='a'*10, message='Hello')
        self.assertEqual(message.sender, 'a'*10)

    # check that message is not created with an empty sender
    def test_sender_empty(self):
        room = Room.objects.create(room_name='room1')
        message = Message(room=room, sender='', message='Hello')
        with self.assertRaises(ValidationError):
            message.full_clean()  # Explicitly validate the model

    # check that message is not created with a sender of length 256
    def test_sender_max_length_plus_one(self):
        room = Room.objects.create(room_name='room1')
        message = Message(room=room, sender='a'*256, message='Hello')
        with self.assertRaises(ValidationError):
            message.full_clean()  # Explicitly validate the model

    # check that message is not created with a null message
    def test_message_empty(self):
        room = Room.objects.create(room_name='room1')
        with self.assertRaises(Exception):
            Message.objects.create(room=room, sender='sender1', message=None)

    # validate __str__ method
    def test_message_str(self):
        room = Room.objects.create(room_name='room1')
        message = Message.objects.create(room=room, sender='sender1', message='Hello')
        self.assertEqual(message.__str__(), 'room1')





















