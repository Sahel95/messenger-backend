# Generated by Django 2.2.3 on 2019-09-03 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_users_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='profile_pic',
            field=models.ImageField(default='pic/defaultpropic.jpg', upload_to='media/'),
        ),
    ]
