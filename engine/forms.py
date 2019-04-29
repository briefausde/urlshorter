from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


# TODO: __init__ duplicate


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control'
            }


class LoginForm(BootstrapMixin, AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')


class RegisterForm(BootstrapMixin, UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
