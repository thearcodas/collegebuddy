# Generated by Django 4.2 on 2023-06-16 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_pyq_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='present',
        ),
        migrations.AddField(
            model_name='attendance',
            name='weightage',
            field=models.IntegerField(default=0),
        ),
    ]
