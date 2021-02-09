from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
import time

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
    ('DC', 'Washington D.C.'),
	('WI', 'Wisconsin'),
	('WY', 'Wyoming')
)
CATEGORY_CHOICES=(
    ('GA', 'ADVICE & RESOURCES-GENERAL'),
    ('CA', 'ADVICE & RESOURCES-CAREER'),
    ('WC', 'BIPOC IN TECH'),
    ('CC', 'CAREER CHANGER'),
    ('CD', 'CAREER DEVELOPMENT'),
    ('EN', 'ENTREPRENEURSHIP'),
    ('WP', 'IN THE WORKPLACE'),
    ('QA', 'Q & A'),
    ('MO', 'MOMMY IN TECH'),
    ('NW', 'NETWORKING'),
    ('NT', 'NEW TO TECH'),
    ('SH', 'TECH SISTERHOOD'),
    ('TC', 'TECH TALK'),
)



class Reply(models.Model):
    post=models.TextField(validators=[MinLengthValidator(2, "Please submit a reply of with at least 2 characters")])
    avatar= models.BinaryField(null=True, editable=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User, related_name='reply_post')
    
    def get_absolute_url(self):
        return reverse("discussion_detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return self.post + ' | ' + str(self.author) 

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering=['-created_at']


class Discussion(models.Model):
    title= models.CharField(max_length= 500, validators=[MinLengthValidator(3, "Please create a title greater than 3 characters")])
    post=models.TextField()
    category= models.CharField(max_length=50,choices=CATEGORY_CHOICES, default=[0][0])
    posted_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    slug = models.SlugField
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    likes =models.ManyToManyField(User, related_name='discussion_post')
    replies= models.ManyToManyField(Reply, related_name='reply')
    

    def __str__(self):
        return str(self.title)

    def __str__(self):
        return self.title + ' | ' + str(self.posted_by)

    def total_likes(self):
        return self.likes.count()


    class Meta:
        ordering=['-created_at']

class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'profile')
    bio =models.TextField(max_length=500, blank=True)
    first_name=models.CharField(max_length=50, blank=True)
    last_name=models.CharField(max_length=50, blank=True)
    email=models.CharField(max_length=50, blank=True) 
    location= models.CharField(max_length=50,choices=STATE_CHOICES, default=[0][0])
    it_area=models.CharField(max_length=50, choices=AREAS, default=[0][0])
    date_joined=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    discussions=models.ManyToManyField(Discussion, related_name='posts')
    replies= models.ManyToManyField(Reply, related_name='replies')

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

class Photo(models.Model):
    url = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Avatar for profile_id:{self.profile_id} @{self.url}"