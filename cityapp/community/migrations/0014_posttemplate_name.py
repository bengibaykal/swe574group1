# Generated by Django 2.2.7 on 2019-11-24 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0013_auto_20191124_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttemplate',
            name='name',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]