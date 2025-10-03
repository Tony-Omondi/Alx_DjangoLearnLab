from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm

def home(request):
    return render(request, 'blog/base.html', {'title': 'Welcome to Django Blog'})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form, 'title': 'Register'})

def user_login(request):
    from django.contrib.auth.views import LoginView
    # Customizing LoginView directly in the view for simplicity
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('blog:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'blog/login.html', {'title': 'Login'})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('blog:home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('blog:profile')
        else:
            messages.error(request, 'Profile update failed. Please correct the errors.')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form, 'title': 'Profile'})