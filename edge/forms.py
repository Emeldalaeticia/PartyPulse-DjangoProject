

from django import forms
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, UserType




class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=UserType.choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'contact_number']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)