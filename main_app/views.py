from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Profile, Discussion, Reply
from django.views.generic import ListView

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def profile(request):
    profile=Profile.objects.all()
    return render(request, 'account/profile.html', {'profile': profile})

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user= user_form.save()
            user.refresh_from_db()
            profile_form=ProfileForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
            login(request, user)
        return redirect('profile')
    else:
        user_form=UserCreationForm()
        profile_form=ProfileForm()
    return render(request, 'registration/signup.html',{
        'user_form': user_form,
        'profile_form':profile_form
    })
class DiscussionListView(ListView):
    model=Discussion
    template_name= 'main_app/discussion_detail.html'
    
# @login_required
# @transaction
# def update_profile(request, user_id):
#     user=User.objects.get(pk=user_id)
#     user.profile.bio= 'Please enter your bio here'



def stream_file(request, pk):
   profile= get_object_or_404(Profile, id=pk)
   response= HttpResponse()
   response['Content-Type']= profile.content_type
   response['Content-Length']=len(profile.avatar)
   response.write(profile.avatar)
   return response 