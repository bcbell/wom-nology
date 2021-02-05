# from django.forms import ModelForm
# from .models import Discussion
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User
from .models import Profile


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
  

class ProfileForm(forms.ModelForm):

    class Meta:
        model= Profile
        fields=['first_name','last_name', 'email',  'location', 'it_area','bio']

    def clean_avatar(self):
        avatar=self.cleaned_data['avatar']
        

        try:
            w, h= get_image_dimensions(avatar)

            max_width=max_height=100
            if w> max_width or h > max_height:
                raise forms.ValidationError(u'Please use an image that is ' "%s x %s pixels or smaller." %(max_width, max_height))
            
            main, sub =avatar.content_type.split('/')
            if not(main=='image' and sub in ['jpeg', 'pjeg', 'gif', 'png']):
                raise forms.ValidationError (u'Please use a JPEG, GIF or PNG image.')

            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(u'Avatar file size may not exceed 20k.')

        except AttributeError:
            pass

        return avatar

    

        
# class Discussion(ModelForm):
#     class Meta:
#         model =Discussion
#         fields= ['title', 'post', 'posted_by']