# Generated by Django 2.1.5 on 2020-04-03 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20200403_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screen',
            name='seat_pattern',
        ),
    ]
