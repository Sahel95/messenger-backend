# Generated by Django 2.2.3 on 2019-09-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20190903_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='media/%y/%m/%d/'),
        ),
    ]
