from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserAccount, UserProfile

class UserForm(UserCreationForm):
    '''
    Form that uses built-in UserCreationForm to handle user creation
    '''
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': '*First name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': '*Last name'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': '*Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Password', 'class': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password', 'class': 'password'}))
    is_staff = forms.BooleanField(required=False)
    is_realtor = forms.BooleanField(required=False)

    # recaptcha token
    token = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = UserAccount
        fields = {'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_realtor'}


class AuthForm(AuthenticationForm):
    '''
    Form that uses built-in AuthenticationForm to handle user auth
    '''
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': '*Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*Password', 'class': 'password'}))

    class Meta:
        model = UserAccount
        fields = {'email', 'password'}


class UserProfileForm(forms.ModelForm):
    '''
    Basic model-form for our user profile that extends Django usermodel
    '''
    address = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())
    town = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())
    country = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())
    post_code = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())
    longitude = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())
    latitude = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = {'address', 'town', 'country', 'post_code', 'country', 'longitude', 'latitude', }