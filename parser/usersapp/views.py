from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistrationForm
from .models import CiteUser
# Create your views here.


class UserLoginView(LoginView):
    template_name = 'usersapp/login.html'


class CreateRegistrateView(CreateView):
    model = CiteUser
    template_name = 'usersapp/createregistrate.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')
