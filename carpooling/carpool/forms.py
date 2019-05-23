from django import forms
from django.core.validators import RegexValidator
from django.shortcuts import render

from .models import Offer, SeatRequest, SeatApprovalRejection



class CreateOfferForm(forms.ModelForm):
    select_regularity = Offer.REGULARITY
    select_districts = Offer.DISTRICTS
    select_seats = Offer.NUMBER_OF_SEATS
    select_contact = Offer.TYPE_OF_CONTACT


    # driver = forms.CharField(widget=forms.Select(attrs={
    #     'class': 'form-control'
    # }))
    start_location = forms.ChoiceField(choices=select_districts,
                             widget=forms.Select(
                                 attrs={
                                     'class': 'form-control'
                                 }
                             ))

    # start_location = forms.ModelChoiceField(required=True, queryset=Offer.objects.values_list('start_location'), widget=forms.TextInput(attrs={
    #     'class': 'form-control'
    # }))
    destination = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    departure_time = forms.TimeField(required=True, widget=forms.TimeInput(
        attrs={
            'class': 'form-control'
        }
    ))
    return_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={
            'class': 'form-control'
        }
    ))
    route = forms.CharField(max_length=400, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    # regularity = forms.MultipleChoiceField(choices=select_regularity,widget=forms.SelectMultiple(
    #                              attrs={
    #                                  'class': 'form-control'
    #                              }
    #                          ))
    regularity = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        queryset = Offer.objects.only('regularity'))



    type_of_contact = forms.ChoiceField(choices=select_contact,
                             widget=forms.Select(
                                 attrs={
                                     'class': 'form-control'
                                 }
                             ))
    number_of_seats = forms.ChoiceField(choices=select_seats,
                             widget=forms.Select(
                                 attrs={
                                     'class': 'form-control'
                                 }
                             ))
    passenger = forms.CharField(max_length=70, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    terms_and_conditions = forms.BooleanField()

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(CreateOfferForm, self).__init__(*args, **kwargs)
    #     # self.fields['regularity'] = forms.ModelChoiceField(queryset=Offer.objects.values('regularity'), widget=forms.SelectMultiple)
    #     for name, field in self.fields.items():
    #         attr = {'class': 'form-control'}
    #         if field.label:
    #             attr['placeholder'] = field.label
    #         field.widget.attrs.update(attr)


    class Meta:
        model = Offer
        fields = ['start_location', 'destination', 'departure_time', 'return_time', 'route', 'regularity', 'type_of_contact', 'number_of_seats', 'passenger', 'terms_and_conditions']
        exclude = ['user', ]
        # widgets = {
        #     'driver': settings.AUTH_USER_MODEL
        # }
     #
    def __init__(self, user, *args, **kwargs):
        super(CreateOfferForm, self).__init__(*args, **kwargs)
        self.fields['regularity'].choices = [(str(item.id), str(item)) for item in Offer.objects.only('regularity')]


# def form_valid(self, form):
#     form.instance.driver = self.request.user
#     return super(CreateOfferForm, self).form_valid(form)


class RequestRideForm(forms.ModelForm):
    ride_id = forms.ModelChoiceField(required=True, queryset=Offer.objects.values_list('pk', flat=True), widget=forms.Select(attrs={
        'class': 'form-control'
    }))
