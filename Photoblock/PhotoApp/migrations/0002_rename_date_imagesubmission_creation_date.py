# Generated by Django 4.2.7 on 2024-02-02 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagesubmission',
            old_name='date',
            new_name='creation_date',
        ),
    ]
