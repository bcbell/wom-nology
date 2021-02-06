# Generated by Django 3.1.6 on 2021-02-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20210206_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='discussions',
            field=models.ManyToManyField(related_name='posts', to='main_app.Discussion'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='replies',
            field=models.ManyToManyField(related_name='replys', to='main_app.Reply'),
        ),
    ]