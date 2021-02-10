# Generated by Django 3.1.6 on 2021-02-10 03:05

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(3, 'Please create a title greater than 3 characters')])),
                ('post', models.TextField()),
                ('category', models.CharField(choices=[('GA', 'ADVICE & RESOURCES-GENERAL'), ('CA', 'ADVICE & RESOURCES-CAREER'), ('WC', 'BIPOC IN TECH'), ('CC', 'CAREER CHANGER'), ('CD', 'CAREER DEVELOPMENT'), ('EN', 'ENTREPRENEURSHIP'), ('WP', 'IN THE WORKPLACE'), ('QA', 'Q & A'), ('MO', 'MOMMY IN TECH'), ('NW', 'NETWORKING'), ('NT', 'NEW TO TECH'), ('SH', 'TECH SISTERHOOD'), ('TC', 'TECH TALK')], default=0, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('likes', models.ManyToManyField(related_name='discussion_post', to=settings.AUTH_USER_MODEL)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('avatar', models.BinaryField(editable=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='reply_post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('location', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('DC', 'Washington D.C.'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default=0, max_length=50)),
                ('it_area', models.CharField(choices=[('IT', 'Information Technology'), ('BI', 'Business Intelligence'), ('CS', 'Cyber Security'), ('C', 'Cloud'), ('DM', 'Data Management'), ('D', 'Database'), ('GD', 'Game Development'), ('GT', 'Geographic IT'), ('HT', 'Healthcare IT'), ('IA', 'IT Audit'), ('IC', 'IT Coordinator'), ('IE', 'IT Executive'), ('IM', 'IT Management'), ('IP', 'IT Project'), ('IS', 'IT Specialist'), ('TT', 'IT Training'), ('N', 'Network'), ('SD', 'Software Developer'), ('SM', 'Software Management'), ('SQ', 'Software Quality'), ('SD', 'System Administator'), ('SA', 'System Analyst')], default=0, max_length=50)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('discussions', models.ManyToManyField(related_name='posts', to='main_app.Discussion')),
                ('replies', models.ManyToManyField(related_name='replies', to='main_app.Reply')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='discussion',
            name='replies',
            field=models.ManyToManyField(related_name='reply', to='main_app.Reply'),
        ),
    ]
