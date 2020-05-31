# Generated by Django 2.2.7 on 2020-05-31 11:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0030_merge_20200517_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='flaggedUsers',
            field=models.ManyToManyField(related_name='flagged_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='flags',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]