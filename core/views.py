import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.urls import reverse
from core.forms import LoginForm, RegisterForm

logger = logging.getLogger(__name__)


# Create your views here.
def fbv_login_view(request):
    form = LoginForm(auto_id=False)
    if request.method == 'POST':
        try:
            email=request.POST['email']
            password=request.POST['password']
            user = authenticate(request=request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            messages.error(request, 'Login Failed')
            return redirect('custom-login', context={'form': form, 'message': 'Login Failed'})
        except Exception as e:
            logger.exception(e)
    return render(request, 'login.html', context={'form': form})


def fbv_logout_view(request):
    logout(request)
    return redirect('home')


class UserResister(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login/'
