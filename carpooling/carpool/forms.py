from django import forms
from django.core.validators import RegexValidator
from .models import Offer, SeatRequest, SeatApprovalRejection


class OfferForm(forms.ModelForm):
    # DISTRICTS = forms.ModelChoiceField(queryset=)
    pass