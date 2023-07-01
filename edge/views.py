from profile import Profile
from .models import UserProfile
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'edge/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('edge:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'edge/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password )
            if user is not None:
                login(request, user)
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
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'edge/profile.html', {'form': form})


