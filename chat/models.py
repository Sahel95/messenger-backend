from django.db import models
from user.models import Users
# from django.contrib.auth.models import User
from datetime import date



class Conversations(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Users, related_name="conversations")
    is_group = models.BooleanField(default=True)
    # last_message = models.TextField(null=True, blank=True)
    date_modified = models.DateField(default=date.today)

    def __str__(self):
        return self.name



class Messages (models.Model):
    sender_id = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="messages")
    conversation_id = models.ForeignKey(
        Conversations,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    text = models.TextField(null=True)
    date = models.DateField()
    picture = models.ImageField(
        upload_to='sent-image/%y/%m/%d/',
        null=True,
        blank=True
    )
    file = models.FileField(
        upload_to='sentfile/%Y/%m/%d/',
        null=True,
        blank=True
    )
    seen = models.BooleanField(default=False)

    # file = models.ImageField()

    def __str__(self):
        return "%s (%s): %s" % (
            self.sender_id.first_name,
            self.conversation_id.name,
            self.text
        )
