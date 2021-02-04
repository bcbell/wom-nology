from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings

#User can have many discussion post 
#User can have many replies to a discussion post
# Create your models here.

#Model Discussion - Foreign Key(User) and ManyToManyField (Reply)

#class Discussion(models.Model):
    #title= models.CharField(max_length= 500, validators=[MinLengthValidator(3, "Please create a title greater than 3 characters")])
    #post=models.TextField()
    #posted_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='discussions_owned')
    #replies= models.ManyToMany(settings.AUTH_USER_MODEL, through='Replies', related_name='discussion_replies')
    #created_at= models.DateTimeField(auto_now_add=True)
    #updated_at= models.DateTimeField(auto_now-True)

    #def __str__(self):
        #return self.title

#Model Reply- Foreign Keys (User and Discussion)

# class Reply(models.Model):
    #post=models.TextField(validators=[MinLengthValidator(2, "Please submit a reply of with at least 2 characters")])
    #picture= models.BinaryField(null=True, editable=True)
    #discussion= models.ForeignKey(Discussion, on_delete=models.CASCADE)
    #posted_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     #created_at= models.DateTimeField(auto_now_add=True)
    #updated_at= models.DateTimeField(auto_now-True)