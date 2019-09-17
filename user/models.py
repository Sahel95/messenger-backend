from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid


class Users(AbstractUser):
    verificationtoken = models.UUIDField(
        default=uuid.uuid4,
        null=True
    )
    is_verified = models.BooleanField(
        null=True,
        default=False
    )
    # token= models.CharField(
    #     null=True,
    #     max_length=200
    # )
    profile_pic = models.ImageField(
        upload_to='profile-pictures',
        null=True,
        blank=True
    )
    contacts = models.ManyToManyField(
        'self',
        related_name='contactlist',
        default=None
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# class ContactList(models.models):
#     user_id = models.ForeignKey(
#         Users,
#         on_delete=models.CASCADE,
#         related_name='name'
#     )
#     members = models.ManyToManyField(Users, related_name='contactlist')
#
#     def __str__(self):
#         return self.user_id
