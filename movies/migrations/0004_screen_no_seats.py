# Generated by Django 2.1.5 on 2020-04-03 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_remove_theater_no_seat'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='no_seats',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]