from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    users = models.ManyToManyField(User)
    hidden = models.BooleanField(default=True)
    name = models.CharField(max_length=255, blank=False, null=True)

    def __str__(self):
        return f'Чат - {self.name}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
