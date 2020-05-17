from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0003_auto_20200501_0751'),
        ('community', '0025_auto_20200426_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='city_id',
            #field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_name', to='city.City'),
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_id', to='city.City')
        ),
    ]
