from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from .models import ProfileUser
from .forms import RegistrationForm

# Create your views here.

#
class SignUp(generic.CreateView):
    model = ProfileUser
    form_class = RegistrationForm
    success_url = '/account/login/'
    # success_url = reverse_lazy('login')
    template_name = 'signup.html'
#
#     # def post(self, request, *args, **kwargs):
#     #     form = RegistrationForm(request.POST)
#     #     if form.is_valid():
#     #         user = form.save()
#     #         user.save()
#     #
#     #     return render(request, 'signup.html', {'form': form})
#

# def signup(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.save()
#             messages.success(request, "Your user is created - Thank you for joining us")
#             login(request, user)
#             success_url = reverse_lazy('login')
#             return redirect(success_url)
#         else:
#             form = RegistrationForm()
#         return render(request, 'signup.html', {'form': form})

#
# def signup(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#         return HttpResponseRedirect("./")
#     else:
#         form = RegistrationForm()
#     return render(request, 'template/register.html', { 'form': form })

    def form_valid(self, form):
        instance = form.save(commit=True)
        instance.user = self.request.user
        instance.save()
        return HttpResponse(status=200)
