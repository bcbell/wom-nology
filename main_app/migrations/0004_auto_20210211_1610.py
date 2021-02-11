# Generated by Django 3.1.6 on 2021-02-11 16:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20210211_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='post',
            field=models.TextField(default=1, validators=[django.core.validators.MinLengthValidator(2, 'Please submit a reply of with at least 2 characters')]),
            preserve_default=False,
        ),
    ]
