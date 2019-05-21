from django import forms
from django.core.validators import RegexValidator

from .models import Offer, SeatRequest, SeatApprovalRejection



class CreateOfferForm(forms.ModelForm):
    select_regularity = Offer.REGULARITY
    select_districts = Offer.DISTRICTS
    select_seats = Offer.NUMBER_OF_SEATS
    select_contact = Offer.TYPE_OF_CONTACT

    ride_id = forms.ModelChoiceField(required=True, queryset=Offer.objects.values_list('pk'), widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))
    # driver = forms.CharField( widget=forms.Select(attrs={
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
    regularity = forms.MultipleChoiceField(choices=select_regularity,widget=forms.SelectMultiple(
                                 attrs={
                                     'class': 'form-control'
                                 }
                             ))

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


    class Meta:
        model = Offer
        fields = '__all__'