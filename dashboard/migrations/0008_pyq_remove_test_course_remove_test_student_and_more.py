# Generated by Django 4.2 on 2023-06-13 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_schedule_unique_together_schedule_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PYQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='question_papers/')),
            ],
        ),
        migrations.RemoveField(
            model_name='test',
            name='course',
        ),
        migrations.RemoveField(
            model_name='test',
            name='student',
        ),
        migrations.AddField(
            model_name='course',
            name='syllabus',
            field=models.FileField(default='syllabuses/default.jpg', upload_to='syllabuses/'),
        ),
        migrations.DeleteModel(
            name='Query',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='pyq',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_papers', to='dashboard.course'),
        ),
    ]