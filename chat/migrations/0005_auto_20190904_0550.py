# Generated by Django 2.2.3 on 2019-09-04 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20190903_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='sent-image/%y/%m/%d/'),
        ),
    ]