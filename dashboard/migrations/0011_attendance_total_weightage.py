# Generated by Django 4.2 on 2023-06-16 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_remove_attendance_present_attendance_weightage'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='total_weightage',
            field=models.IntegerField(default=0),
        ),
    ]