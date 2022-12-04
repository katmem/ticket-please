# Generated by Django 2.1.5 on 2020-04-12 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0018_auto_20200409_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='show',
            field=models.ManyToManyField(to='movies.Show'),
        ),
        migrations.AlterField(
            model_name='screen',
            name='seating_pattern',
            field=models.CharField(choices=[('SEAT_1', 'SEAT_1'), ('SEAT_2', 'SEAT_2')], max_length=255),
        ),
        migrations.AlterField(
            model_name='seat',
            name='status',
            field=models.CharField(choices=[('1', 'Available'), ('2', 'Reserved'), ('3', 'Unavailable')], max_length=20),
        ),
    ]