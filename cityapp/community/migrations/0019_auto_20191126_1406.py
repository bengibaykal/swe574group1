# Generated by Django 2.2.7 on 2019-11-26 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0018_datafilefield_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafilefield',
            name='text_field',
        ),
        migrations.AddField(
            model_name='datafilefield',
            name='file_field',
            field=models.FileField(max_length=55, null=True, upload_to=''),
        ),
    ]
