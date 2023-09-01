from django.contrib import admin
from django.urls import path, include
from . import views




urlpatterns= [
    path('', views.home, name='home page'),
    path('login/', views.loginUser, name='login page'),
    path('signup/', views.registerUser, name='signup page'),
    path('user/', views.userPage, name='user home page'),
    path('logout/', views.logoutUser, name='logout user') ,  
    path('comment/<int:post_id>',views.postComment, name = 'comment on post') ,
    path('addpost/', views.addPost, name='add post') ,
    path('editpost/<int:post_id>', views.editPost, name='edit post'),
    path('deletepost/<int:post_id>', views.deletePost, name='delete post'),
    path('editcomment/<int:post_id>/<int:comment_id>', views.editComment, name='edit comment'),
    path('deletecomment/<int:post_id>/<int:comment_id>', views.deleteComment, name='delete comment'),
    #path('demo/', view=views.demofile, name="demo file"),
    path('edit-profile/<str:username>',views.editProfile, name = 'edit profile'),
    path('follow/<str:username>', views.follow, name = 'follow user'),
    path('unfollow/<str:username>', views.unfollow, name = 'unfollow user'),
    path('followings/<str:username>', views.followings, name = 'users followings'),
    path('followers/<str:username>', views.followers, name = 'users followers'),
    path('user-details/<str:username>', views.user_details, name='user details'),
]

