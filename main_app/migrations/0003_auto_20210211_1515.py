# Generated by Django 3.1.6 on 2021-02-11 15:15

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210210_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='post',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]