from django.urls import path, re_path, include

from . import views

appname = 'accounts'

urlpatterns = [
<<<<<<< HEAD
    re_path(r'^profile/(?P<pk>\d+)/$', views.UserDetail.as_view(), name='user-profile'),
=======
    re_path('profile/(?P<pk>\d+)/', views.UserDetail.as_view(), name='user-profile'),
>>>>>>> ffd12f6a9b299c2a0a74324fd6cfebbe61e671fa
    path('profile/', views.redirect_user, name='profile'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),

]