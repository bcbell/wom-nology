from django.urls import path, reverse_lazy
from . import views


# Need path to read, update, delete, add post, edit post, delete post, profile, update, delete, edit, upload an avatar


urlpatterns= [
#Home and About Pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

#Account Pages
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/discussions/', views.discussionUser, name='user_discussions'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/avatar', views.stream_file, name='avatar'),

#Discussion Pages
    path('discussions/', views.discussionList, name='discussions'),
    path('discussions/<int:discussion_id>/', views.discussionDetail, name='discussion_detail'),
    path('discussions/create', views.discussionCreate, name='discussions_create'),
    path('discussions/<int:pk>/update/', views.DiscussionUpdate.as_view(), name='discussion_update'),
    path('discussions/<int:pk>/delete/', views.DiscussionDelete.as_view(), name='discussion_delete'),

# Reply
    path('discussions/<int:discussion_id>/add_reply', views.add_reply, name='add_reply'),
    path('discussions/<int:pk>/reply/delete/', views.ReplyDelete.as_view(), name='discussion_reply_delete'),

#Likes
    # path('like/<int:pk>', views.Like, name='like'),

#Category
    path('discussions/<str:discussions>/', views.categoryView, name='category'),
    path('discussions/category', views.categoryListView, name='category_list'),

]