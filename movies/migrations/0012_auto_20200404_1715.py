# Generated by Django 2.1.5 on 2020-04-04 14:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0011_auto_20200404_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='hour',
            field=models.TimeField(default=datetime.datetime(2020, 4, 4, 14, 15, 53, 753519, tzinfo=utc)),
        ),
    ]
