from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from posts.models import Post
from followers.models import Follower

def register_view(request: HttpRequest) -> HttpResponse:
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=True)

            login(request, user)

            return redirect('/')

    return render(request, 'accounts/register.html', {'form': form})            

def login_view(request: HttpRequest) -> HttpResponse:
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or '/'

            return redirect(next_url)
        else:
            error_message = "Invalid credentials"
    print(error_message)
    return render(request, 'accounts/login.html', {'error': error_message})    

@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    else:
        return redirect('/')

    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    is_followed = Follower.objects.filter(followed_by=request.user, following=user).exists()
    return render(request, 'profiles/index.html', {"user":user, "posts": posts, "is_followed": is_followed})