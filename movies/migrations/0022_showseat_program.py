# Generated by Django 2.1.5 on 2020-04-12 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0021_auto_20200412_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='showseat',
            name='program',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='movies.Program'),
            preserve_default=False,
        ),
    ]
