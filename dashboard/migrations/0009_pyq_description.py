# Generated by Django 4.2 on 2023-06-14 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_pyq_remove_test_course_remove_test_student_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pyq',
            name='description',
            field=models.TextField(blank=True, default='sample paper', null=True),
        ),
    ]
