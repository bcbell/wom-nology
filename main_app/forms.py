# from django.forms import ModelForm
# from .models import Discussion
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User
from .models import Profile
from .humanize import naturalsize
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import login

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
class CreateForm(forms.ModelForm):
    max_upload_limit= 2* 1024 *1024
    max_upload_limit_text=naturalsize(max_upload_limit)

    avatar=forms.FileField(required=False, label='File to Upload <=' + max_upload_limit_text)
    upload_field_name='avatar'  

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

    #  # Validate the size of the picture
    # def clean(self):
    #     cleaned_data = super().clean()
    #     avatar = cleaned_data.get('avatar')
    #     if avatar is None:return
    #     if len(avatar) > self.max_upload_limit:
    #         self.add_error('avatar', "File must be < "+self.max_upload_limit_text+" bytes")

    # # Convert uploaded File object to a picture
    # def save(self, commit=True):
    #     instance = super(CreateForm, self).save(commit=False)

    #     # We only need to adjust picture if it is a freshly uploaded file
    #     f = instance.avatar   # Make a copy
    #     if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
    #         bytearr = f.read()
    #         instance.content_type = f.content_type
    #         instance.picture = bytearr  # Overwrite with the actual image data

    #     if commit:
    #         instance.save()

    #     return instance

        
# class Discussion(ModelForm):
#     class Meta:
#         model =Discussion
#         fields= ['title', 'post', 'posted_by']