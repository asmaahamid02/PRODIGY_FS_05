from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

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

@login_required
def update_profile_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = UserProfileForm(instance=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save(commit=True)

            return render(request, 'accounts/update_profile.html', {
                'form': form,
                'message': 'Profile updated successfully'
            })

    return render(request, 'accounts/update_profile.html', {'form': form})

@login_required
def change_password_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    form = PasswordChangeForm(user)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            print('valid form')
            form.save(commit=True)

            return render(request, 'accounts/change_password.html',{'form': form, 'message': 'Password has been changed!'})
        
    return render(request, 'accounts/change_password.html',{'form': form})
 