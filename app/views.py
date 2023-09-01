from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post, Post_Comment
from .models import User
from django.contrib.auth.models import Group, Permission, AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm, newUserCreateForm,EditUserProfile
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models.query import QuerySet

def home(request):
    # print(request.user)
    # print(request.user.id )
    # print(request.user.username)
    post_and_comment=[]
    if (isinstance(request.user, AnonymousUser)):
        name='Namaste!!'
        publicgroup, created = Group.objects.get_or_create(name='public')
        if created:
            print("new public group created")
        else:
            print("public group already exist")
        posts = Post.objects.filter(post_group = publicgroup).order_by("-post_last_edited_on")
    elif request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        groups = user.groups.all()
        # print(type(user))
        # print(groups)
        # print(Group.objects.get(name="public").user_set.all())
        name = f"Welcome!!, {user.first_name}"
        posts = None
        for group in groups:
            some_posts = Post.objects.filter(post_group=group)
            if posts is None:
                posts = some_posts
            else:
                posts = posts.union(some_posts)
        posts = posts.order_by("-post_last_edited_on")

    for post in posts:
        comments = Post_Comment.objects.filter(post=post)
        followed = request.user.groups.filter(name=post.user.username).exists()
        post_and_comment.append((post,comments,followed))
    return render(request, 'home.html',{'posts_and_comments':post_and_comment, 'name': name})


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        passwd = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('user not exit')
        user = authenticate(request,username=username,password=passwd)
        if user is not None:
            login(request,user=user)
            return redirect(to='/user')
        else:
            return HttpResponse('Username or Password Not Match')
    else:
        return render(request,'login.html')

def registerUser(request):
    form = newUserCreateForm()
    if request.method == 'POST':
        form = newUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('usercraeted')
            username = form.cleaned_data['username']
            public_group = Group.objects.get(name='public')
            usergroup, created = Group.objects.get_or_create(name=username)
            if created:
                # content_type = ContentType.objects.get_for_model(Post)
                # permission = Permission.objects.create(
                #     codename=username,
                #     name = f"follower of {username}",
                #     content_type=content_type
                # )
                # newgroup.permissions.add(permission)
                # current_user = User.objects.get(username=username)
                # current_user.groups.add(newgroup)
                print("personal group has been created")
                current_user = User.objects.get(username=username)
                public_group.user_set.add(current_user.id)
                usergroup.user_set.add(current_user.id)
                print(f"current user is associated with these groups {current_user.groups.all()}")

            else:
                print("group not created")
        else:
            print('usernotcreated')
        return redirect(to='/login')
    else:
        return render(request, 'signup2.html', {'form': form})
    
@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect(to='/')


@login_required(login_url='/login')
def userPage(request):
    user = request.user
    username = user.username
    current_user = User.objects.get(username=username)
    current_users_all_post = Post.objects.filter(user=current_user).order_by("-post_last_edited_on")
    post_and_comment=[]
    for post in current_users_all_post:
        #print(post.post_group)
        # x =True if post.post_group is None else False
        # print(True if post.post_group is None else False)
        comments = Post_Comment.objects.filter(post=post)
        post_and_comment.append((post,comments))
    return render(request, 'page.html',{'posts_and_comments':post_and_comment, 'username': current_user.username})



@login_required(login_url='/login')
def postComment(request,post_id):
    comment_on_post = request.POST['comment_on_post']
    post = Post.objects.get(id=post_id)
    who_commented = User.objects.get(id=request.user.id)
    comment = Post_Comment(post=post,user=who_commented,comment=comment_on_post)
    comment.save()
    return redirect(to='/')
    

@login_required(login_url='/login')
def addPost(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, 'create_post.html', context={'form':form})
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post_tittle = form.cleaned_data['post_tittle']
            post_content = form.cleaned_data['post_content']
            try:
                post_img = request.FILES['post_img']
            except MultiValueDictKeyError:
                post_img = None
            username = request.user.username
            user = User.objects.get(username=username)
            post_access = form.cleaned_data['post_access']
            if post_access==0:
                post_group = None
            elif post_access==1:
                post_group = Group.objects.get(name="public")
            else:
                post_group = Group.objects.get(name=user.username)
            new_post = Post(user=user, post_tittle=post_tittle, post_img=post_img, post_content=post_content, post_access=post_access, post_group=post_group)
            new_post.save()
            return redirect(to='/user')
    

@login_required(login_url='/login')
def editPost(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            post_title = form.cleaned_data['post_tittle']
            post_img = form.cleaned_data['post_img']
            print(post_img)
            post_content = form.cleaned_data['post_content']
            print()
            post = Post.objects.get(id=post_id)
            print(post.post_img)
            post.post_tittle = post_title
            if post_img == False:
                post.post_img = None
            elif post_img is not None:
                post.post_img = post_img
            post.post_content = post_content
            post_access = form.cleaned_data['post_access']
            if post_access==0:
                post_group = None
            elif post_access==1:
                post_group = Group.objects.get(name="public")
            else:
                post_group = Group.objects.get(name=request.user.username)
            post.post_access = post_access
            post.post_group = post_group
            post.save()


            return redirect(to='/user')
        else:
            return HttpResponse("invalid data")
    
    else:
        form = PostForm(instance=post)
        return render(request, 'edit_post.html',{"form": form, 'post_id':post_id})
    


    
@login_required(login_url='/login')
def deletePost(request, post_id):
    post = Post.objects.get(id=post_id)
    post_user = post.user.id
    if post_user == request.user.id:
        post.delete()
        print('post deleted')
    print("you donot have permission for that")
    return redirect(to='/user')

@login_required(login_url='/login')
def editComment(request, post_id, comment_id):
    comment_user = Post_Comment.objects.get(id=comment_id).user.id
    current_user = User.objects.get(id=request.user.id).id

    if comment_user == current_user:
        comment = Post_Comment.objects.get(id=comment_id)
        form  = CommentForm(instance=comment)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Post_Comment.objects.get(id=comment_id)
                comment.comment = form.cleaned_data['comment']
                comment.save()
            return redirect(to='/')
        else:
            return render(request, 'edit_comment.html', {'form': form})
    else:
        logout(request)
        return redirect(to='/login')
    
@login_required(login_url='/login')
def deleteComment(request, post_id, comment_id):
    comment_user = Post_Comment.objects.get(id=comment_id).user.id
    current_user = User.objects.get(id=request.user.id).id
    post_user = Post.objects.get(id=post_id).user.id


    if comment_user == current_user or current_user==post_user:
        comment = Post_Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect(to='/')

    else:
        logout(request)
        return redirect(to='/login')


# import os
# def demofile(request):
#     # post = Post.objects.get(id=3)
#     # current_dir = os.getcwd()
#     # new_path = os.path.join(current_dir, f"images/{post.post_img.name}")
#     # image_path = post.post_img.path
#     # os.rename(image_path, new_path)
#     # post.save()
#     # print(current_dir)
#     # print(post.post_img.url)
#     # print(request.user.avatar.url)
#     # user = User.objects.get(username="testuser")
#     # print(3421)
#     # print(Group.objects.filter(name="public"))
#     # group  = Group.objects.get(name="public")
#     # for group in group:
#     #     print(user.groups.filter().exists())
#     # print(request.user.get_all_permissions())
#     # print(request.user.has_perm("app.testuser2"))
#     # print(request.user.groups.all())
#     # Group.objects.get(name="public").user_set.get()
#     grp= Group.objects.get(name="public")
#     print(grp.user_set.filter(id=1).exists())
    
#     # print(Group.objects.all().count())
#     # print(Group.objects.get(name='testuser2').user_set.all())
#     return HttpResponse("jus file thing")

@login_required(login_url='/login')
def editProfile(request, username):
    print(username)
    form = EditUserProfile(instance = User.objects.get(username=username))
    if request.method == 'POST':
        form = EditUserProfile(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=username)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.middle_name = form.cleaned_data['middle_name']
            print(form.cleaned_data['avatar'])
            user.avatar = form.cleaned_data['avatar']
            user.save()
            return redirect(to='/user')
    return render(request, 'edit-profile.html', {'form': form})

@login_required(login_url='/login')
def follow(request, username):
    grp= Group.objects.get(name=username)
    grp.user_set.add(request.user.id)
    print("user added to group")
    return redirect(to='/')


@login_required(login_url='/login')
def unfollow(request, username):
    grp= Group.objects.get(name=username)
    grp.user_set.remove(request.user.id)
    print("user has been removed from group")
    return redirect(to='/')

@login_required(login_url='/login')
def followings(request, username):
    user = User.objects.get(username=username)
    grps = user.groups.all()
    print(grps)
    followings = []
    for grp in grps:
        if grp.name != 'public':
            print(grp.name)
            followings.append(grp.name)
    print(followings)
    return render(request, 'user_followings.html', context={"followings" : followings})


@login_required(login_url='/login')
def followers(request, username):
    grp = Group.objects.get(name=username)
    usrs = grp.user_set.all()
    print(usrs)
    return render(request, 'user_followers.html', context={"users":usrs})



@login_required(login_url='/login')
def user_details(request, username):
    user = User.objects.get(username=username)
    users_all_post = Post.objects.filter(user=user).order_by("-post_last_edited_on")
    post_and_comment=[]
    for post in users_all_post:
        comments = Post_Comment.objects.filter(post=post)
        post_and_comment.append((post,comments))
    context = {'posts_and_comments':post_and_comment,"username": user.username, "name": user.first_name, "user_avatar_url": user.avatar.url}
    return render(request, 'user_details.html',context=context)