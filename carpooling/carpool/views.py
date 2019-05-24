from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from accounts.models import ProfileUser
from .models import Offer, SeatRequest, SeatApprovalRejection
from .forms import CreateOfferForm


# Create your views here.

def has_access_to_modify(current_user, current_obj):
    profile_user = ProfileUser.objects.all().filter(user__pk=current_user.id)[0]

    if current_obj.user == profile_user or current_user.is_superuser:
        return True
    return False


def get_all_offers(request):
    # driver = request.GET.get('username')
    offers = Offer.objects.all()
    url = reverse_lazy('carpool:all-offers')
    return HttpResponse(url)


# def create_offer(request):

class CreateOfferView(LoginRequiredMixin, generic.CreateView):
    model = Offer
    form_class = CreateOfferForm
    success_url = reverse_lazy('carpool:my-offers-list')
    template_name = 'create_offer.html'

    def form_valid(self, form):
        user = ProfileUser.objects.all().filter(user__pk=self.request.user.id)[0]
        form.instance.user = user
        return super().form_valid(form)

    def upload_picture(self, request):
        if request.method == 'POST':
            form = CreateOfferForm(request.POST, request.FILES)
            if form.is_valid():
                offer = Offer()
                offer.car_picture = form.cleaned_data['car_picture']
                offer.save()
        return render(request, 'create_offer.html')

    def post(self, request, *args, **kwargs):
        # if request.method == 'POST':
        form = CreateOfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            # offer.driver = ProfileUser.objects.get(user=self.request.user)  # use your own profile here
            offer.user = ProfileUser.objects.get(user=request.user)
            offer.car_picture = form.cleaned_data['car_picture']
            offer.save()
            return HttpResponseRedirect(reverse_lazy('carpool:my-offers-list'))
        return render(request, 'create_offer.html', {'form': form})


class MyOffersView(LoginRequiredMixin, generic.ListView):
    model = Offer
    template_name = 'my_offers.html'
    context_object_name = 'offers'

    def get_queryset(self):
        profile_user = ProfileUser.objects.all().filter(user__pk=self.request.user.id).first()
        offers = Offer.objects.all().filter(user=profile_user)
        if offers:
            return offers
        return []


class OfferDetailView(LoginRequiredMixin, generic.DetailView):
    model = Offer
    login_url = 'accounts/login/'
    context_object_name = 'offers'
    template_name = 'offer_details.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OfferDetailView, self).get_context_data(**kwargs)
        # context['reviews'] = Review.objects.all().filter(offer=self.get_object())

        if has_access_to_modify(self.request.user, self.get_object()):
            context['is_user_offer'] = True
        else:
            context['is_user_offer'] = False

        return context


class AllOffersView(LoginRequiredMixin, generic.ListView):
    model = Offer
    template_name = 'all_offers.html'
    context_object_name = 'offers'

    def get_queryset(self):
        offers = Offer.objects.all()
        if offers:
            return offers
        return []


class OfferDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Offer
    login_url = 'accounts/login/'
    template_name = 'offer_delete.html'
    success_url = reverse_lazy('carpool:my-offers-list')

    def get(self, request, pk):
        if has_access_to_modify(self.request.user, self.get_object()):
            return render(request, 'offer_delete.html', {'offers': self.get_object()})
        return render(request, 'permission_denied.html')

    def post(self, request, pk):
        if not has_access_to_modify(self.request.user, self.get_object()):
            return render(request, 'permission_denied.html')
        furniture = self.get_object()
        furniture.delete()
        return HttpResponseRedirect(reverse_lazy('carpool:my-offers-list'))


class OfferEditView(LoginRequiredMixin, generic.UpdateView):
    model = Offer
    form_class = CreateOfferForm
    template_name = 'create_offer.html'
    success_url = reverse_lazy('carpool:my-offers-list')

    def form_valid(self, form):
        user = ProfileUser.objects.all().filter(user__pk=self.request.user.id)[0]
        form.instance.user = user
        return super().form_valid(form)

    def get(self, request, pk):
        if not has_access_to_modify(self.request.user, self.get_object()):
            return render(request, 'permission_denied.html')
        instance = Offer.objects.get(pk=pk)
        form = CreateOfferForm(request.POST or None, instance=instance)
        return render(request, 'create_offer.html', {'form': form})


class RequestRideView(LoginRequiredMixin, generic.CreateView):
    pass
