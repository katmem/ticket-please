# Generated by Django 2.1.5 on 2020-04-03 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20200403_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='program',
            field=models.ManyToManyField(related_name='shows', to='movies.Program'),
        ),
    ]
