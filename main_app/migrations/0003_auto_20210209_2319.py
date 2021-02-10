# Generated by Django 3.1.6 on 2021-02-09 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210209_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='avatar',
        ),
        migrations.AlterField(
            model_name='profile',
            name='photos',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.photo'),
        ),
    ]
