from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm, DiscussionForm, ReplyForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Profile, Discussion, Reply
from django.views.generic import ListView, DetailView
from .posted import PostedCreateView, PostedUpdatedView, PostedDeleteView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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


def discussionCreate(request):
    form=DiscussionForm()
    if request.method =='POST':
        form=DiscussionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discussions')
    context={'form': form}
    return render(request,'main_app/discussion_form.html', context)

class DiscussionListView(ListView):
    model=Discussion
    def get(self, request):
        ds = Discussion.objects.all()
        replies=[]
        ctx ={'discussion_list': ds, 'replies': replies}
        return render(request, 'discussions/discussion_list.html', ctx)

class DiscussionDetailView(DetailView):
    model=Discussion
    template_name='discussions/discussion_detail.html'
    def get(self, request, pk):
        x=Discussion.objects.get(id=pk)
        replies=Reply.objects.filter(discussion=x).order_by('-updated_at')
        reply_form=ReplyForm()
        context={'discussion': x, 'reply': replies, 'reply_form': reply_form}
        return render(request, self.template_name, context)


    # # def form_valid(self, form):
    # #     form.instance.user=self.request
    # #     return super(DiscussionCreateView, self).form_valid(form)

    # # success_url=reverse_lazy('discussions:all')
    # def get(self, request, pk=None):
    #     form= DiscussionForm()
    #     return render(request, 'main_app/discussion_form.html', {'form': form})

    # def post(self, request, pk=):
    #     form=DiscussionForm(request.POST)

    #     if not form.is_valid():
    #         ctx= {'form': form}
    #         return render(request, self.template_name, ctx)

    #     discussion=form.save(commit=False)
    #     discussion.posted_by=self.user
    #     discussion.save()

    #     return redirect('discussions')


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