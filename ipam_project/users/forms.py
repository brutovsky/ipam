from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    new_password_repeat = forms.CharField(max_length=32, widget=forms.PasswordInput)
