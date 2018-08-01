from django.apps import AppConfig


class CurrencyConfig(AppConfig):
    name = 'currency'

    def ready(self):
        from . import job_scheduler
        job_scheduler.start_jobs()
