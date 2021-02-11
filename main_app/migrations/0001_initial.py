# Generated by Django 3.1.6 on 2021-02-11 16:52

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
                ('category', models.CharField(choices=[('ADVICE & RESOURCES-GENERAL', 'ADVICE & RESOURCES-GENERAL'), ('ADVICE & RESOURCES-CAREER', 'ADVICE & RESOURCES-CAREER'), ('BIPOC IN TECH', 'BIPOC IN TECH'), ('CAREER CHANGER', 'CAREER CHANGER'), ('CAREER DEVELOPMENT', 'CAREER DEVELOPMENT'), ('ENTREPRENEURSHIP', 'ENTREPRENEURSHIP'), ('IN THE WORKPLACE', 'IN THE WORKPLACE'), ('Q & A', 'Q & A'), ('MOMMY IN TECH', 'MOMMY IN TECH'), ('NETWORKING', 'NETWORKING'), ('NEW TO TECH', 'NEW TO TECH'), ('TECH SISTERHOOD', 'TECH SISTERHOOD'), ('TECH TALK', 'TECH TALK')], default='Q & A', max_length=50)),
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
                ('post', models.TextField(validators=[django.core.validators.MinLengthValidator(2, 'Please submit a reply of with at least 2 characters')])),
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
                ('location', models.CharField(choices=[('Alabama', 'Alabama'), ('Alaska', 'Alaska'), ('Arizona', 'Arizona'), ('Arkansas', 'Arkansas'), ('California', 'California'), ('Colorado', 'Colorado'), ('Connecticut', 'Connecticut'), ('Delaware', 'Delaware'), ('Florida', 'Florida'), ('Georgia', 'Georgia'), ('Hawaii', 'Hawaii'), ('Idaho', 'Idaho'), ('Illinois', 'Illinois'), ('Indiana', 'Indiana'), ('Iowa', 'Iowa'), ('Kansas', 'Kansas'), ('Louisiana', 'Louisiana'), ('Maine', 'Maine'), ('Maryland', 'Maryland'), ('Massachusetts', 'Massachusetts'), ('Michigan', 'Michigan'), ('Minnesota', 'Minnesota'), ('Mississippi', 'Mississippi'), ('Missouri', 'Missouri'), ('Montana', 'Montana'), ('Nebraska', 'Nebraska'), ('Nevada', 'Nevada'), ('New Hampshire', 'New Hampshire'), ('New Jersey', 'New Jersey'), ('New Mexico', 'New Mexico'), ('New York', 'New York'), ('North Carolina', 'North Carolina'), ('North Dakota', 'North Dakota'), ('Ohio', 'Ohio'), ('Oklahoma', 'Oklahoma'), ('Oregon', 'Oregon'), ('Pennsylvania', 'Pennsylvania'), ('Rhode Island', 'Rhode Island'), ('South Carolina', 'South Carolina'), ('South Dakota', 'South Dakota'), ('Tennessee', 'Tennessee'), ('Texas', 'Texas'), ('Utah', 'Utah'), ('Vermont', 'Vermont'), ('Virginia', 'Virginia'), ('Washington', 'Washington'), ('Washington D.C.', 'Washington D.C.'), ('Wisconsin', 'Wisconsin'), ('Wyoming', 'Wyoming')], default=0, max_length=50)),
                ('it_area', models.CharField(choices=[('Information Technology', 'Information Technology'), ('Business Intelligence', 'Business Intelligence'), ('Cyber Security', 'Cyber Security'), ('Cloud', 'Cloud'), ('Data Management', 'Data Management'), ('Database', 'Database'), ('Game Development', 'Game Development'), ('Geographic IT', 'Geographic IT'), ('Healthcare IT', 'Healthcare IT'), ('IT Audit', 'IT Audit'), ('IT Coordinator', 'IT Coordinator'), ('IT Executive', 'IT Executive'), ('IT Management', 'IT Management'), ('IT Project', 'IT Project'), ('IT Specialist', 'IT Specialist'), ('IT Training', 'IT Training'), ('Network', 'Network'), ('Software Developer', 'Software Developer'), ('Software Management', 'Software Management'), ('Software Quality', 'Software Quality'), ('System Administator', 'System Administator'), ('System Analyst', 'System Analyst')], default=0, max_length=50)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('linkedin_url', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook_url', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter_url', models.CharField(blank=True, max_length=255, null=True)),
                ('website_url', models.CharField(blank=True, max_length=255, null=True)),
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
