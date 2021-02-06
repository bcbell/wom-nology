from django.urls import path, reverse_lazy
from . import views


# Need path to read, update, delete, add post, edit post, delete post, profile, update, delete, edit, upload an avatar


urlpatterns= [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/avatar', views.stream_file, name='avatar'),
    path('discussions/', views.DiscussionListView.as_view(), name='discussions'),
    path('discussions/<int:pk>/', views.DiscussionDetailView.as_view(), name='discussion_detail'),
    path('discussions/create', views.discussionCreate, name='discussions_create'),

]