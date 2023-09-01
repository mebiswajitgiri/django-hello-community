from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import Post_Comment, Post, User
class demo(forms.Form):
    name = forms.CharField(max_length=100, label="name")
    age = forms.IntegerField(label="age")

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = '__all__'
        exclude = ["user","post_group"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Post_Comment
        fields = ["comment"]

class newUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name' ,'gender', 'email' , 'username' , 'password1', 'password2', 'avatar' ]
class EditUserProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'avatar']
    



