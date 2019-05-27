"""carpooling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from . import settings

from common import views

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('common/', include('common.urls')),
    path('carpool/', include('carpool.urls')),
    path('', views.get_landing_page, name='home'),
    path('FAQ/', views.AllFAQView.as_view(), name='faq'),
    path('FAQ/additem/', views.AddFAQView.as_view(), name='add-faq'),
    re_path('^FAQ/edititem/(?P<pk>\d+)/$', views.EditFAQView.as_view(), name='edit-faq'),
    re_path('^FAQ/deleteitem/(?P<pk>\d+)/$', views.DeleteFAQView.as_view(), name='delete-faq'),
    path('', include('django.contrib.auth.urls')),

]

if settings.DEBUG:

    # urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
