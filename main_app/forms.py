from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Discussion, Reply
from .humanize import naturalsize
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import login


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
class ProfileForm(forms.ModelForm): 
    class Meta:
        model= Profile
        fields=[ 'first_name','last_name', 'email',  'location', 'it_area', 'linkedin_url', 'facebook_url', 'twitter_url','website_url','bio']

class ReplyForm(ModelForm):
    class Meta:
        model=Reply
        fields=['post']


class DiscussionForm(ModelForm):
    class Meta:
        model= Discussion
        fields=['title','category', 'post']


