from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ProfileUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)


    class Meta:
        model = User
        fields = ("first_name", "last_name",  "email", "username","password1", "password2")

        # def clean_username(self):
        #     username = self.cleaned_data["username"]
        #     try:
        #         ProfileUser.objects.get(username=username)
        #     except ProfileUser.DoesNotExist:
        #         return username
        #     raise forms.ValidationError(self.error_messages['duplicate_username'])

    # checks if email is already used and returns message if it's not unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        print(User.objects.filter(email=email).count())
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(f'This email address is already registered.')
        return email

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User")
        user = super(RegistrationForm, self).save(commit=True)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_active = True
        user.is_staff = True
        user.save()

        return user