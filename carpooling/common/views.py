from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse



# Create your views here.

def get_landing_page(request):
    # ('common/templates/landing-page.html')
    return render(request, 'landing-page.html')