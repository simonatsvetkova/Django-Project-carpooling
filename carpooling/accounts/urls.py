from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    # path('signup/', views.signup, name='signup'),

]