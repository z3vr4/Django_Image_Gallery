# Generated by Django 4.2.7 on 2024-02-21 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoApp', '0002_rename_date_imagesubmission_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagesubmission',
            name='title',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='images/defaultimg.png', upload_to='profile_images/'),
        ),
    ]
