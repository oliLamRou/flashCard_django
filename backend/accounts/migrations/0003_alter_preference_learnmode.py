# Generated by Django 5.1.7 on 2025-04-11 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_preference_learnmode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='learnMode',
            field=models.CharField(choices=[('NORMAL', 'Normal'), ('REVERSED', 'Reversed'), ('RANDOM', 'Random')], default='NORMAL', max_length=100),
        ),
    ]
