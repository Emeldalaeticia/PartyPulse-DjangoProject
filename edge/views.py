
from .models import UserProfile, UserType
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'edge/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = form.cleaned_data['user_type']
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('edge:login')  # Redirect to the login page on successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'edge/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Organizer').exists():
                    return redirect('events:organizer_dashboard')
                else:
                    return redirect('events:event_list')
    else:
        form = UserLoginForm()
    return render(request, 'edge/login.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('events:event_list')

@login_required
def profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'edge/profile.html', {'form': form})