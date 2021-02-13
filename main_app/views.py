from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm, DiscussionForm, ReplyForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Profile, Discussion, Reply, Photo
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
import uuid
import boto3
from django.db.models import Q
from django.http import HttpResponseRedirect

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'wom-nology'


def home(request):
    avatar=Photo.objects.all()
    return render(request, 'home.html', {'avatar':avatar})

def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    replies=Reply.objects.all()
    avatar=Photo.objects.all()
    posts=Discussion.objects.filter(posted_by=request.user)
    profile=Profile.objects.all()
    return render(request, 'account/profile.html', {'profile': profile, 'avatar':avatar, 'replies': replies, 'posts':posts})

def discussionDetail(request, discussion_id):
    avatar=Photo.objects.all()
    discussion=Discussion.objects.get(id=discussion_id)
    replies=Reply.objects.filter().order_by('-updated_at')
    reply_form=ReplyForm()
    return render(request, 'main_app/discussion_detail.html', {'discussion': discussion, 'reply_form': reply_form, 'replies':replies, "avatar": avatar})

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
    # avatar=Photo.objects.get()
    posts=Discussion.objects.all()
    return render(request, 'discussions/discussion_list.html', {'posts': posts})

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

@login_required
def add_reply(request, discussion_id):
        form=ReplyForm(request.POST)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.discussion_id=discussion_id
            instance.author_id=request.user.id
            instance.save()
        return redirect('discussion_detail',discussion_id=discussion_id)

  
def add_photo(request):
    avatar=Photo.objects.all()
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile', {'avatar': avatar})

def search(request):
    comments=Discussion.objects.all().order_by('-created_at')
    search_discussions=request.GET.get('search')
    if search_discussions:
        comments=Discussion.objects.filter(Q(title__icontains=search_discussions) | Q(post__icontains=search_discussions))
        return render(request, 'main_app/search_list.html', {'comments': comments})
    else:
        return render(request, 'main_app/search_list.html', {'comments': comments})

def like (request, pk):
    discussion =get_object_or_404(Discussion, id=request.POST.get('discussion_id'))
    discussion.likes.add(request.user)
    return HttpResponseRedirect(reverse('discussion_detail', args=[str(pk)]))

def like (request, pk):
    discussion =get_object_or_404(Discussion, id=request.POST.get('discussion_id'))
    discussion.likes.add(request.user)
    return HttpResponseRedirect(reverse('discussion_detail', args=[str(pk)]))

class DiscussionUpdate(UpdateView):
    model=Discussion
    fields=['title', 'post']

class DiscussionDelete(DeleteView):
    model=Discussion
    success_url='/discussions/'

class ReplyUpdate(UpdateView):
    model=Reply
    fields= ['post']
    success_url='/discussions/'

class ReplyDelete(DeleteView):
    model=Reply
    template_name='main_app/reply_confirm_delete.html'
    success_url='/discussions/'



