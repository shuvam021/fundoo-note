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
