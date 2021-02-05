from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator

# from django.conf import settings

AREAS=(
        ('IT', 'Information Technology'),
        ('BI', 'Business Intelligence'),
        ('CS', 'Cyber Security'),
        ('C', 'Cloud'),
        ('DM', 'Data Management'),
        ('D', 'Database'),
        ('GD', 'Game Development'),
        ('GT', 'Geographic IT'),
        ('HT', 'Healthcare IT'),
        ('IA', 'IT Audit'),
        ('IC', 'IT Coordinator'),
        ('IE', 'IT Executive'),
        ('IM', 'IT Management'),
        ('IP', 'IT Project'),
        ('IS', 'IT Specialist'),
        ('TT', 'IT Training'),
        ('N', 'Network'),
        ('SD', 'Software Developer'),
        ('SM', 'Software Management'),
        ('SQ', 'Software Quality'),
        ('SD', 'System Administator'),
        ('SA', 'System Analyst'),  
    )
STATE_CHOICES = (
	('AL', 'Alabama'),
	('AK', 'Alaska'),
	('AZ', 'Arizona'),
	('AR', 'Arkansas'),
	('CA', 'California'),
	('CO', 'Colorado'),
	('CT', 'Connecticut'),
	('DC', 'Washington D.C.'),
	('DE', 'Delaware'),
	('FL', 'Florida'),
	('GA', 'Georgia'),
	('HI', 'Hawaii'),
	('ID', 'Idaho'),
	('IL', 'Illinois'),
	('IN', 'Indiana'),
	('IA', 'Iowa'),
	('KS', 'Kansas'),
	('LA', 'Louisiana'),
	('ME', 'Maine'),
	('MD', 'Maryland'),
	('MA', 'Massachusetts'),
	('MI', 'Michigan'),
	('MN', 'Minnesota'),
	('MS', 'Mississippi'),
	('MO', 'Missouri'),
	('MT', 'Montana'),
	('NE', 'Nebraska'),
	('NV', 'Nevada'),
	('NH', 'New Hampshire'),
	('NJ', 'New Jersey'),
	('NM', 'New Mexico'),
	('NY', 'New York'),
	('NC', 'North Carolina'),
	('ND', 'North Dakota'),
	('OH', 'Ohio'),
	('OK', 'Oklahoma'),
	('OR', 'Oregon'),
	('PA', 'Pennsylvania'),
	('RI', 'Rhode Island'),
	('SC', 'South Carolina'),
	('SD', 'South Dakota'),
	('TN', 'Tennessee'),
	('TX', 'Texas'),
	('UT', 'Utah'),
	('VT', 'Vermont'),
	('VA', 'Virginia'),
	('WA', 'Washington'),
	('WI', 'Wisconsin'),
	('WY', 'Wyoming')
)

class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'profile')
    avatar=models.ImageField(null=True, editable= True)
    # is_active = models.BooleanField(('active'), default=True)
    bio =models.TextField(max_length=500, blank=True)
    first_name=models.CharField(max_length=50, blank=True)
    last_name=models.CharField(max_length=50, blank=True)
    email=models.CharField(max_length=50, blank=True) 
    location= models.CharField(max_length=50,choices=STATE_CHOICES, default=[0][0])
    it_area=models.CharField(max_length=50, choices=AREAS, default=[0][0])
    date_joined=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#User can have many discussion post 
#User can have many replies to a discussion post
# Create your models here.

#Model Discussion - Foreign Key(User) and ManyToManyField (Reply)

class Discussion(models.Model):
    title= models.CharField(max_length= 500, validators=[MinLengthValidator(3, "Please create a title greater than 3 characters")])
    post=models.TextField()
    posted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions_owned')
    replies= models.ManyToManyField(User, through='Reply', related_name='discussion_replies')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

#Model Reply- Foreign Keys (User and Discussion)

class Reply(models.Model):
    post=models.TextField(validators=[MinLengthValidator(2, "Please submit a reply of with at least 2 characters")])
    avatar= models.BinaryField(null=True, editable=True)
    discussion= models.ForeignKey(Discussion, on_delete=models.CASCADE)
    posted_by=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)