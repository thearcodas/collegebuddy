# Generated by Django 4.2 on 2023-04-21 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_stream_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='stream',
        ),
        migrations.DeleteModel(
            name='Stream',
        ),
    ]
