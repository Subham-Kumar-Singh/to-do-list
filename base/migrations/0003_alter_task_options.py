# Generated by Django 4.1.5 on 2023-02-20 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_task_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['complete'], 'permissions': [('can_view_all_todos', 'Can view all todos')]},
        ),
    ]
