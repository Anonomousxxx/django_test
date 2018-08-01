from currency.models import Currency, ExchangeRate
import itertools
import requests
from django.core.cache import cache
import json
import logging

logger = logging.getLogger("django_apscheduler")


class FetchExchangeRatesJob(object):

    def __init__(self):
        self.session = requests.session()
        self.session.cookies = get_cached_cookies()

    def run(self):
        # load all the current currencies
        currencies = Currency.objects.all()
        # get all possible combinations
        currency_combinations = itertools.combinations(currencies, 2)
        for currency_combination in currency_combinations:
            # try catch in case of some server error or wrong currency codes
            try:
                self.fetch_exchange_rate(list(currency_combination))
            except Exception as e:
                logger.exception(e)

    def fetch_exchange_rate(self, currency_combination):
        # always sort alphabetically to make sure we have only one item in the database
        currency_combination.sort(key=lambda x: x.name)
        url = 'https://api.cryptonator.com/api/ticker/{0}-{1}'.format(currency_combination[0].name.lower(), currency_combination[1].name.lower())
        response = self.session.get(url)
        exchange_rate = response.json()
        cache_cookies(response.cookies)
        price = exchange_rate.get('ticker', {}).get('price')
        if price:
            ExchangeRate.objects.update_or_create(currency_1=currency_combination[0], currency_2=currency_combination[1],
                                                  defaults={'currency_1': currency_combination[0], 'currency_2': currency_combination[1],
                                                            'value': price})


# cache cookies to persist on server restart
def cache_cookies(cookies):
    if cookies:
        cache.set("cookies", json.dumps(requests.utils.dict_from_cookiejar(cookies)))


def get_cached_cookies():
    cached_cookies = cache.get("cookies", "{}")
    return requests.utils.cookiejar_from_dict(json.loads(cached_cookies))
