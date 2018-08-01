# currency URL Configuration

from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda r: redirect('currency/')),
    path('currency/', include('currency.urls')),
    path('admin/', admin.site.urls),
]
