from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .jobs.FetchExchangeRatesJob import FetchExchangeRatesJob
from .models import ExchangeRate, Currency, UserExchangeRate

test_credentials_login = {'username': 'testuser', 'password': 'testpass'}
test_credentials_signup = {'username': 'testuser', 'password1': 'testpass', 'password2': 'testpass'}
test_btc_usd_value = 33.333
test_currency_name_1 = 'RUR'
test_currency_name_2 = 'UAH'
test_currency_value = 66.666


class LoginTest(TestCase):

    def setUp(self):
        User.objects.create_user(**test_credentials_login)

    # test login success and redirect to home
    def test_login(self):
        # send login data
        response = self.client.post(reverse('currency:login'), test_credentials_login, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome")


class SignupTest(TestCase):

    def setUp(self):
        currencies = list(Currency.objects.all())
        currencies.sort(key=lambda x: x.name)
        ExchangeRate.objects.update_or_create(currency_1=currencies[0], currency_2=currencies[1],
                                              defaults={'currency_1': currencies[0], 'currency_2': currencies[1],
                                                        'value': test_btc_usd_value})

    # test that initial btc and usd exchange rate is created on signup
    def test_btc_usd_created_on_signup(self):
        response = self.client.post(reverse('currency:signup'), test_credentials_signup, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1 {0} = {1} {2}'.format("BTC", "{:.10f}".format(test_btc_usd_value), "USD"))


class ExRateTest(TestCase):

    def setUp(self):
        User.objects.create_user(**test_credentials_login)
        self.client.post(reverse('currency:login'), test_credentials_login, follow=True)
        self.currency_1 = Currency.objects.create(name=test_currency_name_1)
        self.currency_2 = Currency.objects.create(name=test_currency_name_2)
        self.exchange_rate = ExchangeRate.objects.create(currency_1=self.currency_1, currency_2=self.currency_2, value=test_currency_value)

    # test adding and removing user exchange rates
    def test_add_remove(self):
        response = self.client.post(reverse('currency:add'), {'currency_1': self.currency_1.pk, 'currency_2': self.currency_2.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1 {0} = {1} {2}'.format(test_currency_name_1, "{:.10f}".format(test_currency_value), test_currency_name_2))
        pk = UserExchangeRate.objects.filter(exchange_rate=self.exchange_rate).first().pk
        response = self.client.post("/currency/delete/{0}".format(pk), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No exchange rates to track')


class FetchExRatesTest(TestCase):
    def setUp(self):
        self.currency_1 = Currency.objects.create(name=test_currency_name_1)
        self.currency_2 = Currency.objects.create(name=test_currency_name_2)

    # test that job fetches the exchange rate and saves it to db
    def test_fetch_exrates_job(self):
        job = FetchExchangeRatesJob()
        job.run()
        self.assertIsNotNone(ExchangeRate.objects.filter(currency_1=self.currency_1, currency_2=self.currency_2).first())
