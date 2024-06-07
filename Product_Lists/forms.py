from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)