# Generated by Django 2.2.3 on 2019-09-04 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20190904_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='sentfile/%Y/%m/%d/'),
        ),
    ]