# Generated by Django 2.1.5 on 2020-04-03 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20200403_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theater',
            name='no_seat',
        ),
    ]
