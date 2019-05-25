from django.urls import path, re_path, include

from . import views

from accounts.views import SignUp

app_name = 'carpool'

urlpatterns = [
    path('create/', views.CreateOfferView.as_view(), name='create-offer'),
    path('alloffers', views.AllOffersView.as_view(), name='all-offers'),
    path('myoffers/', views.MyOffersView.as_view(), name='my-offers-list'),
    re_path('^myoffers/(?P<pk>\d+)/$', views.MyOffersView.as_view(), name='my-offers'),
    re_path('^offerdetails/(?P<pk>\d+)/$', views.OfferDetailView.as_view(), name='offer-details'),
    re_path('^delete/(?P<pk>\d+)/$', views.OfferDeleteView.as_view(), name='offer-delete'),
    re_path('^edit/(?P<pk>\d+)/$', views.OfferEditView.as_view(), name='offer-edit'),
    path('request/', views.RequestRideView.as_view(), name='request-ride'),
    re_path('^myrequests/(?P<pk>\d+)/$', views.MyRequestsView.as_view(), name='my-requests'),
    path('myrequests/', views.MyRequestsView.as_view(), name='my-requests-list'),
    re_path('^requestdetails/(?P<pk>\d+)/$', views.RequestDetailView.as_view(), name='request-details'),
    re_path('^requestdelete/(?P<pk>\d+)/$', views.RequestDeleteView.as_view(), name='request-delete'),
    path('allrequests', views.AllRequestsView.as_view(), name='all-requests'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('signup/', SignUp.as_view(), name='signup'),
]