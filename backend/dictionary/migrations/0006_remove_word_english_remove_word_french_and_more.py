# Generated by Django 5.1.7 on 2025-04-23 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0005_alter_word_word_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='english',
        ),
        migrations.RemoveField(
            model_name='word',
            name='french',
        ),
        migrations.RemoveField(
            model_name='word',
            name='korean',
        ),
    ]
