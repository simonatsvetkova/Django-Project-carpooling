from django.urls import path, re_path, include

from . import views

app_name = 'carpool'

urlpatterns = [
    path('create/', views.CreateOfferView.as_view(), name='create-offer'),
    path('alloffers', views.AllOffersView.as_view(), name='all-offers'),
    path('myoffers/', views.MyOffersView.as_view(), name='my-offers-list'),
    re_path('^myoffers/(?P<pk>\d+)/$', views.MyOffersView.as_view(), name='my-offers'),
    re_path('^offerdetails/(?P<pk>\d+)/$', views.OfferDetailView.as_view(), name='offer-details'),
    re_path('^delete/(?P<pk>\d+)/$', views.OfferDeleteView.as_view(), name='offer-delete'),
    re_path('^edit/(?P<pk>\d+)/$', views.OfferEditView.as_view(), name='offer-edit'),
    re_path('^request/(?P<pk>\d+)/$', views.RequestRideView.as_view(), name='request-ride'),

]