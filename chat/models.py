from django.conf import settings
from django.db import models

class Conversation(models.Model):
    create_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="created_conversations")
    create_realtor = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="realtor_conversations")

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

class ProblemReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Problem by {self.user.username}: {self.description[:20]}"