from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy

from accounts.models import ProfileUser
from .models import Offer, SeatRequest, SeatApprovalRejection
from .forms import CreateOfferForm

# Create your views here.

def has_user_access_to_modify(current_user, current_obj):
    profile_user = ProfileUser.objects.all().filter(user__pk=current_user.id)[0]

    if current_obj.user == profile_user or current_user.is_superuser:
        return True
    return False


def get_all_offers(request):
    # driver = request.GET.get('username')
    offers = Offer.objects.all()
    return HttpResponse(offers)

# def create_offer(request):

class CreateOfferView(LoginRequiredMixin, generic.CreateView):
    model = Offer
    form_class = CreateOfferForm
    # success_url = '/accounts/login/'
    success_url = reverse_lazy('my-offers')
    template_name = 'create_offer.html'

    # def get_initial(self):
    #     return {
    #         'driver': Offer.objects.all().filter(user=ProfileUser.driver).first()
    #     }

    # def get(self, request, *args, **kwargs):
    #     context = {'form': CreateOfferForm()}
    #     return render(request, 'create_offer.html', context)

    def form_valid(self, form):
        user = ProfileUser.objects.all().filter(user__pk=self.request.user.id)[0]
        form.instance.user = user
        return super().form_valid(form)

    # @login_required
    def post(self, request, *args, **kwargs):

        form = CreateOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            # offer.driver = ProfileUser.objects.get(user=self.request.user)  # use your own profile here
            offer.user = request.user
            offer.save()
            return HttpResponseRedirect(reverse_lazy('my-offers'))
        return render(request, 'create_offer.html', {'form': form})


class MyOffersView(generic.ListView):
    model = Offer
    template_name = 'my_offers.html'
    context_object_name = 'offers'

    def get_queryset(self):
        profile_user = ProfileUser.objects.all().filter(user__pk=self.request.user.id).first()
        offers = Offer.objects.all().filter(user = profile_user)
        if offers:
            return offers
        return []


# class OfferDetailView(LoginRequiredMixin, generic.DetailView):
#     model = Offer
#     login_url = 'accounts/login/'
#     context_object_name = 'offers'
#     template_name = 'offer_details.html'
#
#
#     def get_context_data(self, object_list=None, **kwargs):
#         context = super(OfferDetailView, self).get_context_data(**kwargs)
#         context['reviews'] = Review.objects.all().filter(offer=self.get_object())
#
#         if has_user_access_to_modify(self.request.user, self.get_object()):
#             context['is_user_offer'] = True
#         else:
#             context['is_user_offer'] = False
#
#         return context

