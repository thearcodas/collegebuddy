# Generated by Django 4.2 on 2023-04-19 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
