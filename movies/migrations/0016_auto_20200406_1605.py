# Generated by Django 2.1.5 on 2020-04-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_show_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]