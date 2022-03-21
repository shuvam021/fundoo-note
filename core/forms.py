from cProfile import label
from logging import PlaceHolder
from django import forms
from api.authentication.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}),
            'password': forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})
        }
        labels = {
            'email': '',
            'password': '',
        }


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}),
            'last_name': forms.TextInput(attrs={"placeholder": "LastName", "class": "form-control"}),
            'email': forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}),
            'password': forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
        }
