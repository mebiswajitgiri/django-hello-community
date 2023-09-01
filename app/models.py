from django.db import models
from django.contrib.auth.models import  AbstractUser, Group
# Create your models here.



class User(AbstractUser):
    gender_choice = [('M', 'Male'), ('F', "Female"), ('O', 'Others')]
    first_name = models.CharField(max_length=100,blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(null=True, unique=True)
    avatar = models.ImageField(null=True, upload_to='profile_imgs', default='man.png', blank=True)
    gender = models.CharField(max_length=10,choices=gender_choice, default='O')


class Post(models.Model):
    access_type = [
        (1, 'Public'),
        (0, 'Private'),
        (10, 'Only Followers')
    ]
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    post_tittle =  models.CharField("Title",max_length=50, null=True, blank=True)
    post_img =  models.ImageField("Images",upload_to='post_imgs/', null=True,blank=True,default=None)
    post_content =  models.TextField("Content", null=True)
    post_created_on = models.DateTimeField(auto_now_add=True,null=True)
    post_last_edited_on = models.DateTimeField(auto_now=True, null=True)
    post_group  = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True,default=None)
    post_access = models.IntegerField(null=True, choices=access_type)

class Post_Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField(null=True)
    commented_on = models.DateTimeField(auto_now_add=True,null=True)
    comment_edited_on = models.DateTimeField(auto_now=True, null=True)



    






