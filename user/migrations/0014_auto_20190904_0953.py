# Generated by Django 2.2.3 on 2019-09-04 09:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_users_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='members',
        ),
        migrations.AddField(
            model_name='users',
            name='contacts',
            field=models.ManyToManyField(related_name='_users_contacts_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
