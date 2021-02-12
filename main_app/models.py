from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
import time
# from ckeditor.fields import RichTextField



AREAS=(
        ('Information Technology', 'Information Technology'),
        ('Business Intelligence', 'Business Intelligence'),
        ('Cyber Security', 'Cyber Security'),
        ('Cloud', 'Cloud'),
        ('Data Management', 'Data Management'),
        ('Database', 'Database'),
        ('Game Development', 'Game Development'),
        ('Geographic IT', 'Geographic IT'),
        ('Healthcare IT', 'Healthcare IT'),
        ('IT Audit', 'IT Audit'),
        ('IT Coordinator', 'IT Coordinator'),
        ('IT Executive', 'IT Executive'),
        ('IT Management', 'IT Management'),
        ('IT Project', 'IT Project'),
        ('IT Specialist', 'IT Specialist'),
        ('IT Training', 'IT Training'),
        ('Network', 'Network'),
        ('Software Development', 'Software Development'),
        ('Software Management', 'Software Management'),
        ('Software Quality', 'Software Quality'),
        ('System Administation', 'System Administation'),
        ('System Analyst', 'System Analyst'),  
    )
STATE_CHOICES = (
	('Alabama', 'Alabama'),
	('Alaska', 'Alaska'),
	('Arizona', 'Arizona'),
	('Arkansas', 'Arkansas'),
	('California', 'California'),
	('Colorado', 'Colorado'),
	('Connecticut', 'Connecticut'),
	('Delaware', 'Delaware'),
	('Florida', 'Florida'),
	('Georgia', 'Georgia'),
	('Hawaii', 'Hawaii'),
	('Idaho', 'Idaho'),
	('Illinois', 'Illinois'),
	('Indiana', 'Indiana'),
	('Iowa', 'Iowa'),
	('Kansas', 'Kansas'),
	('Louisiana', 'Louisiana'),
	('Maine', 'Maine'),
	('Maryland', 'Maryland'),
	('Massachusetts', 'Massachusetts'),
	('Michigan', 'Michigan'),
	('Minnesota', 'Minnesota'),
	('Mississippi', 'Mississippi'),
	('Missouri', 'Missouri'),
	('Montana', 'Montana'),
	('Nebraska', 'Nebraska'),
	('Nevada', 'Nevada'),
	('New Hampshire', 'New Hampshire'),
	('New Jersey', 'New Jersey'),
	('New Mexico', 'New Mexico'),
	('New York', 'New York'),
	('North Carolina', 'North Carolina'),
	('North Dakota', 'North Dakota'),
	('Ohio', 'Ohio'),
	('Oklahoma', 'Oklahoma'),
	('Oregon', 'Oregon'),
	('Pennsylvania', 'Pennsylvania'),
	('Rhode Island', 'Rhode Island'),
	('South Carolina', 'South Carolina'),
	('South Dakota', 'South Dakota'),
	('Tennessee', 'Tennessee'),
	('Texas', 'Texas'),
	('Utah', 'Utah'),
	('Vermont', 'Vermont'),
	('Virginia', 'Virginia'),
	('Washington', 'Washington'),
    ('Washington D.C.', 'Washington D.C.'),
	('Wisconsin', 'Wisconsin'),
	('Wyoming', 'Wyoming')
)
CATEGORY_CHOICES=(
    ('ADVICE & RESOURCES-GENERAL', 'ADVICE & RESOURCES-GENERAL'),
    ('ADVICE & RESOURCES-CAREER', 'ADVICE & RESOURCES-CAREER'),
    ('BIPOC IN TECH', 'BIPOC IN TECH'),
    ('CAREER CHANGER', 'CAREER CHANGER'),
    ('CAREER DEVELOPMENT', 'CAREER DEVELOPMENT'),
    ('ENTREPRENEURSHIP', 'ENTREPRENEURSHIP'),
    ('IN THE WORKPLACE', 'IN THE WORKPLACE'),
    ('Q & A', 'Q & A'),
    ('MOMMY IN TECH', 'MOMMY IN TECH'),
    ('NETWORKING', 'NETWORKING'),
    ('NEW TO TECH', 'NEW TO TECH'),
    ('TECH SISTERHOOD', 'TECH SISTERHOOD'),
    ( 'TECH TALK', 'TECH TALK'),
)



class Reply(models.Model):
    post=models.TextField(validators=[MinLengthValidator(2, "Please submit a reply of with at least 2 characters")])
    # post=RichTextField(blank=True, null=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    likes=models.ManyToManyField(User, related_name='reply_post')
    
    def get_absolute_url(self):
        return reverse("discussion_detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return str(self.author)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering=['-created_at']


class Discussion(models.Model):
    title= models.CharField(max_length= 500, validators=[MinLengthValidator(3, "Please create a title greater than 3 characters")])
    post=models.TextField()
    category= models.CharField(max_length=50,choices=CATEGORY_CHOICES, default='Q & A')
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

class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Avatar for profile_id:{self.user.id} @{self.url}"

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
    # avatar=models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='pic', null=True)
    linkedin_url=models.CharField(max_length=255, null=True, blank=True)
    facebook_url=models.CharField(max_length=255, null=True, blank=True)
    twitter_url=models.CharField(max_length=255, null=True, blank=True)
    website_url=models.CharField(max_length=255, null=True, blank=True)

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


    
    