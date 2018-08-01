from django import forms
from .models import Currency, ExchangeRate, UserExchangeRate


class ExchangeRateCreateForm(forms.Form):

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    currency_1 = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        empty_label=None,
        label='',
    )
    currency_2 = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        empty_label=None,
        label=''
    )

    def clean(self):
        cleaned_data = super().clean()
        currency_1 = cleaned_data.get("currency_1")
        currency_2 = cleaned_data.get("currency_2")

        if currency_1 == currency_2:
            raise forms.ValidationError("Currencies should be different!")

        is_reversed = False
        currencies = [currency_1, currency_2]
        currencies_sorted = sorted(currencies, key=lambda x: x.name)
        if currencies != currencies_sorted:
            is_reversed = True

        exchange_rate = ExchangeRate.objects.filter(currency_1=currencies_sorted[0], currency_2=currencies_sorted[1]).first()
        if not exchange_rate:
            raise forms.ValidationError("No data about this exchange rate yet")

        user_exchange_rate = UserExchangeRate.objects.filter(user=self.user, exchange_rate=exchange_rate, reversed=is_reversed).first()
        if user_exchange_rate:
            raise forms.ValidationError("User already has this exchange rate!")
        self.cleaned_data.update({'exchange_rate': exchange_rate, "reversed": is_reversed})

    def save(self):
        exchange_rate = self.cleaned_data.get('exchange_rate')
        is_reversed = self.cleaned_data.get('reversed')
        UserExchangeRate.objects.create(exchange_rate=exchange_rate, reversed=is_reversed, user=self.user)
