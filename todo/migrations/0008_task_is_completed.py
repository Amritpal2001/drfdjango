# Generated by Django 3.1.5 on 2021-05-01 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_completedtask_moderator'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
