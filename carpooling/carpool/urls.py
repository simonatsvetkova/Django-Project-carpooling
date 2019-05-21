from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('create/', views.CreateOfferView.as_view(), name='create-offer'),

]