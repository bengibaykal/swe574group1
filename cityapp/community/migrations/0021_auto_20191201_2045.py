# Generated by Django 2.2.7 on 2019-12-01 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0020_post_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postdatatype',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='postdatatype',
            name='data_char_field',
        ),
        migrations.RemoveField(
            model_name='postdatatype',
            name='data_date_field',
        ),
        migrations.RemoveField(
            model_name='postdatatype',
            name='data_float_field',
        ),
        migrations.RemoveField(
            model_name='postdatatype',
            name='data_image_field',
        ),
        migrations.RemoveField(
            model_name='postdatatype',
            name='data_location_field',
        ),
        migrations.RemoveField(
            model_name='postdatatype',
            name='data_text_field',
        ),
        migrations.RemoveField(
            model_name='post',
            name='data_type',
        ),
        migrations.DeleteModel(
            name='DataCharField',
        ),
        migrations.DeleteModel(
            name='DataDateField',
        ),
        migrations.DeleteModel(
            name='DataFloatField',
        ),
        migrations.DeleteModel(
            name='DataImageField',
        ),
        migrations.DeleteModel(
            name='DataLocationField',
        ),
        migrations.DeleteModel(
            name='DataTextField',
        ),
        migrations.DeleteModel(
            name='PostDataType',
        ),
    ]