# Generated by Django 2.2.3 on 2019-09-04 09:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20190904_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='contacts',
            field=models.ManyToManyField(default=None, null=True, related_name='_users_contacts_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
