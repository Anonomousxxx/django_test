from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    currency_1 = models.ForeignKey(Currency, related_name='exchangerate_currency1', on_delete=models.CASCADE)
    currency_2 = models.ForeignKey(Currency, related_name='exchangerate_currency2', on_delete=models.CASCADE)
    value = models.FloatField()

    class Meta:
        unique_together = ('currency_1', 'currency_2')

    def __str__(self):
        return '1 {0} = {1} {2}'.format(self.currency_1, "{:.10f}".format(self.value), self.currency_2)


class UserExchangeRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange_rate = models.ForeignKey(ExchangeRate, on_delete=models.CASCADE)
    reversed = models.BooleanField()

    class Meta:
        unique_together = ('user', 'exchange_rate', 'reversed')

    def __str__(self):
        if not self.reversed:
            return '1 {0} = {1} {2}'.format(self.exchange_rate.currency_1,
                                            "{:.10f}".format(self.exchange_rate.value),
                                            self.exchange_rate.currency_2)
        else:
            return '1 {0} = {1} {2}'.format(self.exchange_rate.currency_2,
                                            "{:.10f}".format(1 / self.exchange_rate.value),
                                            self.exchange_rate.currency_1)
