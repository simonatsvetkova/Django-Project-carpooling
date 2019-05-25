from django.urls import path, re_path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^profile/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user-profile'),
    # re_path('profile/(?P<pk>\d+)/', views.UserDetail.as_view(), name='user-profile'),
    path('profile/', views.redirect_user, name='profile'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('', include('carpool.urls', namespace='carpool'))

]