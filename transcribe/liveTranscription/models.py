from django.db import models


class Session(models.Model):
    session_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_name

    def clean(self):
        if not self.session_name:
            raise ValueError("Session name should not be empty")
        if len(self.session_name) > 255:
            raise ValueError("Session name should not be greater than 255 characters")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Transcription(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
    )
    transcription = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.transcription
