# Generated by Django 2.1.5 on 2020-04-12 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0022_showseat_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='program',
            field=models.ManyToManyField(to='movies.Program'),
        ),
    ]
