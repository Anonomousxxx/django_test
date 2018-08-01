from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import ExchangeRate, UserExchangeRate, Currency
from .forms import ExchangeRateCreateForm


@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'exchange_rates'

    def get_queryset(self):
        return UserExchangeRate.objects.filter(user=self.request.user).all()


@login_required()
def delete_exrate(request, exrate_id):
    UserExchangeRate.objects.get(pk=exrate_id).delete()
    return redirect('currency:home')


@login_required()
def add_exrate(request):
    if request.method == 'POST':
        form = ExchangeRateCreateForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('currency:home')
    else:
        form = ExchangeRateCreateForm()

    return render(request, 'add.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            init_on_signup(user)
            return redirect('currency:home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# add initial btc/usd exchange rate on sign up
def init_on_signup(user):
    btc_currency = Currency.objects.filter(name='BTC').first()
    usd_currency = Currency.objects.filter(name='USD').first()
    exchange_rate = ExchangeRate.objects.filter(currency_1=btc_currency, currency_2=usd_currency).first()
    if exchange_rate:
        UserExchangeRate.objects.create(exchange_rate=exchange_rate, reversed=False, user=user)
