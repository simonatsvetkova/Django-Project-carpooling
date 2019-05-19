from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ProfileUser


class RegistrationForm(UserCreationForm):
    # username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)

    # password1 = forms.CharField(required=True)
    # password2 = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

        # def clean_username(self):
        #     username = self.cleaned_data["username"]
        #     try:
        #         ProfileUser.objects.get(username=username)
        #     except ProfileUser.DoesNotExist:
        #         return username
        #     raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(RegistrationForm, self).save(commit=True)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_active = True
        user.is_staff = True
        user.save()

        # if commit:
        #     user.save()
        return user

    # def save(self, commit=True):
    #     user = User.objects.create_user(
    #         self.cleaned_data['username'],
    #         self.cleaned_data['email'],
    #         self.cleaned_data["first_name"],
    #         self.cleaned_data["last_name"],
    #         self.cleaned_data['password1']
    #     )
    #     user.is_active = True
    #     return user
