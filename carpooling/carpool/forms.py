from django import forms

from .models import Offer, SeatRequest


class CreateOfferForm(forms.ModelForm):
    select_regularity = Offer.REGULARITY
    select_districts = Offer.DISTRICTS
    select_seats = Offer.NUMBER_OF_SEATS
    select_contact = Offer.TYPE_OF_CONTACT

    start_location = forms.ChoiceField(choices=select_districts,
                                       widget=forms.Select(
                                           attrs={
                                               'class': 'form-control'
                                           }
                                       ))
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
    regularity = forms.MultipleChoiceField(choices=select_regularity, widget=forms.SelectMultiple(
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
    car_picture = forms.ImageField(required=False, label='Upload image')
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
        fields = ['start_location', 'destination', 'departure_time', 'return_time', 'route', 'regularity',
                  'type_of_contact', 'number_of_seats', 'passenger', 'car_picture', 'terms_and_conditions']

    def __init__(self, *args, **kwargs):
        super(CreateOfferForm, self).__init__(*args, **kwargs)
        self.fields['regularity'].widget = forms.CheckboxSelectMultiple(choices=Offer.REGULARITY)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


class EditOfferForm(forms.ModelForm):
    select_regularity = Offer.REGULARITY
    select_districts = Offer.DISTRICTS
    select_seats = Offer.NUMBER_OF_SEATS
    select_contact = Offer.TYPE_OF_CONTACT

    start_location = forms.ChoiceField(choices=select_districts,
                                       widget=forms.Select(
                                           attrs={
                                               'class': 'form-control'
                                           }
                                       ))
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
    regularity = forms.MultipleChoiceField(choices=select_regularity, widget=forms.SelectMultiple(
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
    car_picture = forms.ImageField(required=False, label='Upload image')

    class Meta:
        model = Offer
        fields = ['start_location', 'destination', 'departure_time', 'return_time', 'route', 'regularity',
                  'number_of_seats', 'passenger', 'car_picture', 'terms_and_conditions']

    def __init__(self, *args, **kwargs):
        super(EditOfferForm, self).__init__(*args, **kwargs)
        self.fields['regularity'].widget = forms.CheckboxSelectMultiple(choices=Offer.REGULARITY)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


class RequestRideForm(forms.ModelForm):
    ride_id = forms.ModelChoiceField(queryset=Offer.objects.all(),
                                     widget=forms.Select(attrs={
                                         'class': 'form-control'
                                     }))

    comments = forms.CharField(max_length=400, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    terms_and_conditions = forms.BooleanField()

    class Meta:
        model = SeatRequest
        fields = ['ride_id', 'comments', 'terms_and_conditions']
        exclude = ['passenger']
