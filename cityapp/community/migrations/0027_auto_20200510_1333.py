# Generated by Django 2.2.7 on 2020-05-10 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0026_community_city_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='city_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_id', to='city.City'),
        ),
    ]
