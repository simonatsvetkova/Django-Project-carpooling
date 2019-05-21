from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


from .models import Offer, SeatRequest, SeatApprovalRejection
from .forms import CreateOfferForm

# Create your views here.

class CreateOfferView(generic.CreateView):
    model = Offer
    form_class = CreateOfferForm
    # success_url = '/accounts/login/'
    success_url = reverse_lazy('my-offers')
    template_name = 'create_offer.html'