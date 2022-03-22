import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from core.forms import LoginForm, RegisterForm

logger = logging.getLogger(__name__)


# Create your views here.
def fbv_login_view(request):
    form = LoginForm(auto_id=False)
    if request.method == 'POST':
        try:
            user = authenticate(
                request=request,
                email=request.POST['email'],
                password=request.POST['password']
            )
            if user is not None:
                login(request, user)
                return redirect('profile')
            messages.error(request, 'Login Failed')
            return redirect('custom-login')
        except Exception as e:
            logger.exception(e)
    return render(request, 'forms.html', context={'form': form, 'title': 'Login'})


def fbv_logout_view(request):
    logout(request)
    return redirect('home')


class UserResister(CreateView):
    form_class = RegisterForm
    template_name = 'forms.html'
    success_url = '/login/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Register'
        return data
