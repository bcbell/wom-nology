# Generated by Django 3.1.6 on 2021-02-07 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0013_discussion_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='discussion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.discussion'),
        ),
    ]
