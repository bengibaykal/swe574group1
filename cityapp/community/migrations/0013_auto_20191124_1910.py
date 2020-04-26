# Generated by Django 2.2.7 on 2019-11-24 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0012_auto_20191124_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttemplate',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='community_template', to='community.Community'),
        ),
        migrations.AddField(
            model_name='posttemplate',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='template_author', to=settings.AUTH_USER_MODEL),
        ),
    ]