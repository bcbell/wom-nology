from django.urls import path
from . import views


# Need path to read, update, delete, add post, edit post, delete post, profile, update, delete, edit, upload an avatar


urlpatterns= [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/avatar', views.stream_file, name='avatar')

]