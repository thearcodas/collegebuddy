# Generated by Django 4.2 on 2023-06-10 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_schedule_time'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('stream', 'semester', 'day', 'time')},
        ),
    ]
