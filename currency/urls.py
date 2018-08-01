# currency URL Configuration

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'currency'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('delete/<int:exrate_id>', views.delete_exrate, name='delete'),
    path('add', views.add_exrate, name='add'),
    path('login', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout', auth_views.logout, {'next_page': 'currency:login'}, name='logout'),
    path('signup', views.signup, name='signup'),
]
