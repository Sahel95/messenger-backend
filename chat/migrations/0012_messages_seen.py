# Generated by Django 2.2.3 on 2019-09-15 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0011_remove_conversations_last_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
