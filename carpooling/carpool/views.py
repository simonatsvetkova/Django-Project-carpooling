from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from accounts.models import ProfileUser
from .models import Offer, SeatRequest, SeatApprovalRejection
from .forms import CreateOfferForm, RequestRideForm, EditOfferForm


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


# def create_offer(request):

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
        try:
            offer = Offer.objects.get(pk=pk)
            # offer = self.get_object()
            offer.delete()
        except Exception as error:
            print(f"cant delete --> {error}")
        return HttpResponseRedirect(reverse_lazy('carpool:my-offers-list'))
'''
def edit_offer(request, pk):
    offer = Offer.objects.get(id=pk)
    print(f"offer --> {offer}")
    print(f"offer id --> {offer.id}")
    print(f"offer_ID --> {pk}")
    start_location = offer.start_location
    destination = offer.destionation
    departure_time = offer.departure_time
    return_time = offer.return_time
    route = offer.route
    regularity = offer.regularity
    number_of_seats = offer.number_of_seats
    passenger = offer.passenger
    if request.method != 'POST':
        form = EditOfferForm(instance=offer)
    else:
        form = EditOfferForm(instance=offer, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('carpool:my-offers-list'))
    context = {'offer': offer, 'start_location': start_location, 'destination': destination, 'departure_time': departure_time, 'return_time': return_time, 'route': route, 'regularity': regularity, 'number_of_seats': number_of_seats, 'passenger': passenger}
    return render(request, 'edit_offer.html', context)
'''



class OfferEditView(LoginRequiredMixin, generic.UpdateView):
    model = Offer
    form_class = CreateOfferForm
    template_name = 'edit_offer.html'
    success_url = reverse_lazy('carpool:my-offers-list')
    context_object_name = 'offer'


    def form_valid(self, form):
        user = ProfileUser.objects.all().filter(user__pk=self.request.user.id)[0]
        form.instance.user = user
        return super().form_valid(form)

    # def get_object(self, queryset=None):
    #
    #     # get the existing object or created a new one
    #     obj, created = Offer.objects.get_or_create(col_1=self.kwargs['user'], col_2=self.kwargs['pk'])
    #     print(f"object --> {obj}")
    #     print(f"created --> {created}")
    #     return obj


    def get(self, request, pk):
        if has_access_to_modify(self.request.user, self.get_object()):
            instance = Offer.objects.get(pk=pk)
            offer = CreateOfferForm(request.POST or None, instance=instance)
            return render(request, 'edit_offer.html', {'offers': self.get_object()})
            # getting error with the below row -- Reverse for 'offer-edit' with arguments '('',)' not found. 1 pattern(s) tried: ['carpool\\/edit/(?P<pk>\\d+)/$']
            # return render(request, 'edit_offer.html', {'offers': offer})

        return render(request, 'permission_denied.html')


    def post(self, request, pk):
        if not has_access_to_modify(self.request.user, self.get_object()):
            return render(request, 'permission_denied.html')
        try:
            offer = Offer.objects.get(pk=pk)
            # offer = self.get_object()
            offer.save()
        except Exception as error:
            print(f"cant edit --> {error}")
        return HttpResponseRedirect(reverse_lazy('carpool:my-offers-list'))






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

