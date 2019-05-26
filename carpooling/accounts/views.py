from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ProfileUser
from .forms import RegistrationForm


# Create your views here.

def redirect_user(request):
    url = f'carpool:my-offers-list'
    return redirect(url)


def has_access_to_modify(current_user, current_obj):
    profile_user = ProfileUser.objects.all().filter(user__id=current_user.id).first()
    print(f"current user id --> {profile_user.id}")
    if current_obj.user == profile_user or current_user.is_superuser:
        return True
    return False



class UserDetail(View):
    model = ProfileUser
    template_name = 'user_profile.html'
    context_object_name = 'user'

    def get(self, request, username):
        profile_user = ProfileUser.objects.all().filter(user__id=self.request.user.id).first()
        if str(self.request.user) == str(profile_user):
            return render(request, 'user_profile.html')
        else:
            return render(request, 'permission_denied.html')



class SignUp(generic.CreateView):
    model = ProfileUser
    form_class = RegistrationForm
    # success_url = '/accounts/login/'
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    #
    ##### error on saving. use the save from the models.py
    # def post(self, request, *args, **kwargs):
    #     # if request.method == 'POST':
    #     form = RegistrationForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         profile = form.save(commit=False)
    #         profile.user = ProfileUser.objects.get(user=request.user)
    #         profile.first_name = form.cleaned_data['first_name']
    #         profile.last_name = form.cleaned_data['last_name']
    #         profile.username = form.cleaned_data['username']
    #         profile.email = form.cleaned_data['email']
    #         profile.profile_picture = form.cleaned_data['profile_picture']
    #         profile.save()
    #         return HttpResponseRedirect(reverse_lazy('accounts:login'))
    #     return render(request, 'signup.html', {'form': form})
    #
