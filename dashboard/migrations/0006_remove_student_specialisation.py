# Generated by Django 4.2 on 2023-04-21 03:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_course_professor_assigned_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='specialisation',
        ),
    ]