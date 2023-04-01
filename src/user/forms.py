from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserModel


class CustomUserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email', 'password1', 'password2']


class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class EmailForm(forms.Form):
    email = forms.EmailField()


class ForgotPasswordForm(forms.Form):
    code = forms.CharField(max_length=6)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


