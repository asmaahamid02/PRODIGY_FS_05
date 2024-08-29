from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserProfileForm
from posts.models import Post
from followers.models import Follower
from django.db.models import Q, Exists, OuterRef

@login_required
def update_profile_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = UserProfileForm(instance=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save(commit=True)

            return render(request, 'profiles/update.html', {
                'form': form,
                'message': 'Profile updated successfully'
            })

    return render(request, 'profiles/update.html', {'form': form})

@login_required
def change_password_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = PasswordChangeForm(user)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            print('valid form')
            form.save(commit=True)

            return render(request, 'profiles/change_password.html',{'form': form, 'message': 'Password has been changed!'})
        
    return render(request, 'profiles/change_password.html',{'form': form})
 
@login_required
def profile_view(request: HttpRequest, username:str) -> HttpResponse:
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    is_followed = Follower.objects.filter(followed_by=request.user, following=user).exists()
    return render(request, 'profiles/index.html', {"user":user, "posts": posts, "is_followed": is_followed})

@login_required
def suggested_users_view(request: HttpRequest) -> HttpResponse:
    user = request.user

    followers = Follower.objects.filter(followed_by=user)
    usersToExclude = [follower.following.id for follower in followers]

    users = User.objects.exclude(Q(pk__in=usersToExclude) | Q(pk=user.id)).annotate(
        following_you = Exists(Follower.objects.filter(followed_by=OuterRef('pk'), following=user))
    ).order_by('username')

    return render(request, 'profiles/users.html', {"users": users})