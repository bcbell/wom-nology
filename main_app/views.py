from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm, DiscussionForm, ReplyForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Profile, Discussion, Reply
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
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
    return render(request, 'discussions/discussion_list.html', {'posts': posts})

def discussionDetail(request, discussion_id, reply_id):
    post=Discussion.object.get(id='discussion_id')
    reply=Reply.objects.get(id='reply_id')
    # reply_form=ReplyForm()
    return render(request, 'discussions/discussion_detail.html', {'post': post, 'reply': reply})

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

def replyCreate(request):        
    form=ReplyForm()
    if request.method =='POST':
        form= ReplyForm(request.POST)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.posted_by=request.user 
            # instance.discussion_id=request.user.profile.discussions.filter(id=id)
            instance.save()
            return redirect('discussions')
    context={'form': form}
    return render(request, 'main_app/reply_form.html', context)


   
#    def add_avatar(request):
#     form = ReplyForm()
#     if request.method == 'POST':
#         form=ReplyForm(da)
    # post=Discussion.object.get(id='discussion_id')
    # reply=Reply.objects.get(id='reply_id')
    # form=ReplyForm(request.POST or None)
    # if form.is_valid():
    #     instance =form.save(commit=False)
    #     form.instance.discussion_id=self.kwargs['pk']
    #     instance.posted_by=request.user
    #     instance.save()
    #     return redirect('discussions')
    # return render(request,'main_app/reply_form.html', {'form': form, 'post': post, 'reply': reply})

def Like (request, pk):
    post=get_object_or_404(Discussion, id=discussion_id)
    liked= False
    if post.likes.filter(id=request.user):
        post.likes.remove(request.user)
        liked= False
    else:
        post.likes.add(request.user)
        liked=True
    return HttpRepsonseRedirect(reverse)

def categoryListView(request):
    discussion_menu_list= Category.objects.all()
    return render(request, {'category': category })

def categoryView(request, discussions):
    categories= Discussion.objects.filter('categories')
    return render(request, {'categories': categories})

class DiscussionDetail(DetailView):
    model=Discussion
    fields='__all__'

    # def get_context_data(self, discussion):
    #     like=get_object_or_404(Discussion, id=discussion_id)
    #     total_likes=likes.total_likes

    #     liked= False
    #     if like.likes.filter(id=self.id):
    #         liked=True
        
    #     context['total_likes']= total_likes
    #     context['liked']=liked
    #     return context

class DiscussionUpdate(UpdateView):
    model=Discussion
    fields=['title', 'post']

class DiscussionDelete(DeleteView):
    model=Discussion
    success_url='/discussions/'

class ReplyCreate(CreateView):
    model=Reply
    form_class= ReplyForm
    template_name= 'reply_form.html'
    
    def replyCreate(self, request):        
    # form=ReplyForm()
    # if request.method =='POST':
    #     form= ReplyForm(request.POST)
        if form.is_valid():
            instance =form.save(commit=False)
            instance.posted_by=request.user
            instance.discussion_id=self.kwargs['pk']
            instance.save()
        success_url = reverse_lazy('discussions')   
    #     return redirect('discussions')
    # context={'form': form}
    # return render(request, 'main_app/reply_form.html', context)


    # def form_valid(self, form):
    #     pk=Discussion.objects.get('id')
    #     form.instance.discussion_id= self.kwargs=[pk]
    #     return super().form_valid(form)
    
    # success_url = reverse_lazy('discussions') 

    # def get(self, request):
    #     form=ReplyForm()
    #     context= {'form': form}

    # def post(self, request):
    #     form= ReplyForm(request.POST)
    #     if not form.is_valid():
    #         context={'form': form}
    #         return render(request, self.template, context)

    #     reply=form.save()
    #     return redirect(self.success_url)

    # def form_valid(self, form):
    #     posts=Reply.objects.filter(posted_by=request.user)
    #     instance.posted_by=request.user
    #     form.instance.discussion_id=self.kwargs['pk']
    #     return super().form_valid(form, posts, instance)

    # success_url = reverse_lazy('discussions')

class ReplyDelete(DeleteView):
    model=Reply
    success_url= reverse_lazy('discussions')

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