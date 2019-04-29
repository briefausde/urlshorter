from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


# TODO: __init__ duplicate


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control'
            }

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control'
            }

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
