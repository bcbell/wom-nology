from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm, DiscussionForm, ReplyForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Profile, Discussion, Reply
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    profile=Profile.objects.all()
    return render(request, 'account/profile.html', {'profile': profile})

@login_required
def discussionUser(request):
    posts=Discussion.objects.filter(posted_by=request.user)
    return render(request, 'account/user_discussions.html', {'posts': posts})

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

def discussionList(request):
    posts=Discussion.objects.all()
    # posts=Discussion.objects.filter(id='discussion_id')
    return render(request, 'discussions/discussion_list.html', {'posts': posts})

def discussionDetail(request, discussion_id):
    post=Discussion.object.get(id='discussion_id')
    reply_form=ReplyForm()
    return render(request, 'discussions/discussion_detail.html', {'post': post, 'reply_form': reply_form})

@login_required
def discussionCreate(request):
    form=DiscussionForm(request.POST or None)
    if form.is_valid():
        instance =form.save(commit=False)
        instance.posted_by=request.user
        instance.save()
        return redirect('discussions')
    context={'form': form}
    return render(request,'main_app/discussion_form.html', context)

class DiscussionDetail(DetailView):
    model=Discussion
    fields='__all__'

class DiscussionUpdate(UpdateView):
    model=Discussion
    fields=['title', 'post']

class DiscussionDelete(DeleteView):
    model=Discussion
    success_url='/discussions/'

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