# Generated by Django 2.2.3 on 2019-09-01 11:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20190901_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='verificationtoken',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
