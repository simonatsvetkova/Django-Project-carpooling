from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from accounts.models import ProfileUser
from .models import Offer, SeatRequest, SeatApprovalRejection
from .forms import CreateOfferForm

# Create your views here.

class CreateOfferView(generic.CreateView):
    model = Offer
    form_class = CreateOfferForm
    # success_url = '/accounts/login/'
    success_url = reverse_lazy('my-offers')
    template_name = 'create_offer.html'

    def form_valid(self, form):
        offer = form.save(commit=False)
        # offer.driver = ProfileUser.objects.get(user=self.request.user)  # use your own profile here
        offer.driver = self.request.user
        offer.save()
        return HttpResponseRedirect(self.get_success_url())

