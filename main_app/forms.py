from django.forms import ModelForm
# from .models import Discussion
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Discussion
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
        fields=[ 'first_name','last_name', 'email',  'location', 'it_area','bio']

class ReplyForm(forms.Form):
    reply= forms.CharField(required=True, max_length=500, min_length=3, strip=True) 

class DiscussionForm(forms.Form):
    class Meta:
        model= Discussion
        fields=[ 'title','post', 'posted_by']

# #     max_upload_limit= 2* 1024 *1024
# #     max_upload_limit_text=naturalsize(max_upload_limit)

# #     avatar=forms.FileField(required=False, label='File to Upload:' + max_upload_limit_text)
# #     upload_field_name='avatar'

# #  # Validate the size of the picture
# #     def clean(self):
# #         cleaned_data = super().clean()
# #         avatar = cleaned_data.get('avatar')
# #         if avatar is None:return
# #         if len(avatar) > self.max_upload_limit:
# #             self.add_error('avatar', "File must be < "+self.max_upload_limit_text+" bytes")

# #     # Convert uploaded File object to a picture
# #     def save(self, commit=True):
# #         instance = super(ProfileForm, self).save(commit=False)

# #         # We only need to adjust picture if it is a freshly uploaded file
# #         f = instance.avatar   # Make a copy
# #         if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
# #             bytearr = f.read()
# #             instance.content_type = f.content_type
# #             instance.picture = bytearr  # Overwrite with the actual image data

# #         if commit:
# #             instance.save()

# #         return instance
