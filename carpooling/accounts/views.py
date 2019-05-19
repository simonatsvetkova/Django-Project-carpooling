from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from .models import ProfileUser
from .forms import RegistrationForm


# Create your views here.

def redirect_user(request):
    url = f'/offers/'
    return HttpResponseRedirect(url)


class UserDetail(generic.DetailView):
    model = ProfileUser
    template_name = 'user_profile.html'
    context_object_name = 'user'


class SignUp(generic.CreateView):
    model = ProfileUser
    form_class = RegistrationForm
    # success_url = '/accounts/login/'
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
