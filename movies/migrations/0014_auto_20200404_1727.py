# Generated by Django 2.1.5 on 2020-04-04 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_auto_20200404_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='hour',
            field=models.TimeField(default=datetime.datetime.now),
        ),
    ]
