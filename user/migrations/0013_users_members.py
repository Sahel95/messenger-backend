# Generated by Django 2.2.3 on 2019-09-04 09:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20190904_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='members',
            field=models.ManyToManyField(related_name='_users_members_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
