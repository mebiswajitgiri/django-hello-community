from django.contrib import admin

# Register your models here.
from .models import Post_Comment, Post, User

admin.site.register([Post_Comment,Post, User])