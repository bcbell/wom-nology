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

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'wom-nology'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    profile=Profile.objects.all()
    avatar=Photo.objects.all()
    return render(request, 'account/profile.html', {'profile': profile, 'avatar':avatar})

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
    return render(request, 'discussions/discussion_list.html', {'posts': posts})

def discussionDetail(request, discussion_id):
    discussion=Discussion.objects.get(id=discussion_id)
    reply=Reply.objects.filter(id__in=discussion.replies.all().values_list('id'))
    reply_form=ReplyForm()
    return render(request, 'main_app/discussion_detail.html', {'discussion': discussion, 'reply_form': reply_form, 'reply':reply})

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
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, user_id=user_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('profile', avatar)


#   if form.is_valid():
# #         instance =form.save(commit=False)
# #         form.instance.discussion_id=self.kwargs['pk']
# #         instance.posted_by=request.user
# #         instance.save()
#     form = ReplyForm()
#     if request.method == 'POST':
#         form=ReplyForm(da)
#     post=Discussion.object.get(id='discussion_id')
#     reply=Reply.objects.get(id='reply_id')
#     form=ReplyForm(request.POST or None)
#     if form.is_valid():
#         instance =form.save(commit=False)
#         form.instance.discussion_id=self.kwargs['pk']
#         instance.posted_by=request.user
#         instance.save()
#         return redirect('discussions')
#     return render(request,'main_app/reply_form.html', {'form': form, 'post': post, 'reply': reply})

# def Like (request, pk):
#     post=get_object_or_404(Discussion, id=discussion_id)
#     liked= False
#     if post.likes.filter(id=request.user):
#         post.likes.remove(request.user)
#         liked= False
#     else:
#         post.likes.add(request.user)
#         liked=True
#     return HttpRepsonseRedirect(reverse)

def categoryListView(request):
    category= Discussion.objects.all()
    return render(request,'discussions/category_list.html', {'category': category })

def categoryView(request, discussions):
    categories= Discussion.objects.filter('category')
    return render(request, 'discussions/category_list.html', {'categories': categories})

class CategoryListView(ListView):
    model=Discussion
    fields=['category']
    template_name='discussions/category_list.html'

# class CategoryDetail(DetailView):
#     model=Discussion
#     fields='__all__'
#     template_name='discussions/category_detail.html'


class DiscussionDetail(DetailView):
    model=Discussion
    fields='__all__'

 
    def get_context_data(self, discussion):
        like=get_object_or_404(Discussion, id=discussion_id)
        total_likes=likes.total_likes

        liked= False
        if like.likes.filter(id=self.id):
            liked=True
        
        context['total_likes']= total_likes
        context['liked']=liked
        return context

class ProfileUpdate(UpdateView):
    model=Profile
    template_name='account/profile.html'
    fields=['first_name', 'last_name', 'bio','email', 'location', 'it_area']

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



