# Generated by Django 4.2.4 on 2023-08-15 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='type',
        ),
    ]
