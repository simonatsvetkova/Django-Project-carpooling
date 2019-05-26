from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from accounts.models import ProfileUser
from .forms import CreateOfferForm, RequestRideForm
from .models import Offer, SeatRequest


# Create your views here.

def has_access_to_modify(current_user, current_obj):
    profile_user = ProfileUser.objects.all().filter(user__pk=current_user.id).first()

    if current_obj.user == profile_user or current_user.is_superuser:
        return True
    return False


def get_all_offers(request):
    # driver = request.GET.get('username')
    offers = Offer.objects.all()
    url = reverse_lazy('carpool:all-offers')
    return HttpResponse(url)



class CreateOfferView(LoginRequiredMixin, generic.CreateView):
    model = Offer
    form_class = CreateOfferForm
    success_url = reverse_lazy('carpool:my-offers-list')
    template_name = 'create_offer.html'

    def form_valid(self, form):
        user = ProfileUser.objects.all().filter(user__pk=self.request.user.id).first()
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
    offers_count = Offer.objects.count()

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
        try:
            offer = Offer.objects.get(pk=pk)
            offer.delete()
        except Exception as error:
            print(f"cant delete --> {error}")
        return HttpResponseRedirect(reverse_lazy('carpool:my-offers-list'))



class OfferEditView(LoginRequiredMixin, generic.UpdateView):
    model = Offer
    form_class = CreateOfferForm
    template_name = 'edit_offer.html'
    success_url = reverse_lazy('carpool:my-offers-list')
    context_object_name = 'offers'

    def dispatch(self, request, *args, **kwargs):
        handler = super(OfferEditView, self).dispatch(request, *args, **kwargs)
        # Only allow editing if current user is owner
        if str(self.object.user) == str(request.user) or request.user.is_superuser:
            return handler
        return render(request, 'permission_denied.html')



class RequestRideView(LoginRequiredMixin, generic.CreateView):
    model = SeatRequest
    form_class = RequestRideForm
    template_name = 'request_ride.html'
    success_url = reverse_lazy('carpool:my-requests-list')


    def post(self, request, *args, **kwargs):
        form = RequestRideForm(request.POST)
        if form.is_valid():
            ride_request = form.save(commit=False)
            ride_request.user = ProfileUser.objects.get(user=request.user)
            ride_request.save()
            return HttpResponseRedirect(reverse_lazy('carpool:my-requests-list'))
        return render(request, 'request_ride.html', {'form': form})






class MyRequestsView(LoginRequiredMixin, generic.ListView):
    model = SeatRequest
    template_name = 'my_requests.html'
    context_object_name = 'request'

    def get_queryset(self):
        profile_user = ProfileUser.objects.all().filter(user__pk=self.request.user.id).first()
        offers = SeatRequest.objects.all().filter(user=profile_user)
        if offers:
            return offers
        return []


class AllRequestsView(LoginRequiredMixin, generic.ListView):
    model = SeatRequest
    template_name = 'all_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        requests = SeatRequest.objects.all()
        if requests:
            return requests
        return []



class RequestDetailView(LoginRequiredMixin, generic.DetailView):
    model = SeatRequest
    login_url = 'accounts/login/'
    context_object_name = 'requests'
    template_name = 'request_details.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(RequestDetailView, self).get_context_data(**kwargs)
        # context['reviews'] = Review.objects.all().filter(offer=self.get_object())

        if has_access_to_modify(self.request.user, self.get_object()):
            context['is_user_offer'] = True
        else:
            context['is_user_offer'] = False

        return context



class RequestDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = SeatRequest
    login_url = 'accounts/login/'
    template_name = 'request_delete.html'
    success_url = reverse_lazy('carpool:my-requests-list')

    def get(self, request, pk):
        if has_access_to_modify(self.request.user, self.get_object()):
            return render(request, 'request_delete.html', {'requests': self.get_object()})
        return render(request, 'permission_denied.html')

    def post(self, request, pk):
        if not has_access_to_modify(self.request.user, self.get_object()):
            return render(request, 'permission_denied.html')
        ride_request = self.get_object()
        ride_request.delete()
        return HttpResponseRedirect(reverse_lazy('carpool:my-requests-list'))

