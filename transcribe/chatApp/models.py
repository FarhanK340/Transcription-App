from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=255, null = False, blank = False, unique= True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Validate the model before saving
        super().save(*args, **kwargs)

class Message(models.Model):
    room = models.ForeignKey(
        Room,
        # related_name='messages',
        on_delete=models.CASCADE
    )
    sender = models.CharField(max_length=255, null = False, blank = False) 
    message = models.TextField(null = False, blank = False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.room)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)