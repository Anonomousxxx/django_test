from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from .jobs.FetchExchangeRatesJob import FetchExchangeRatesJob

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", seconds=10, replace_existing=True)
def fetch_exchange_rates_job():
    job = FetchExchangeRatesJob()
    job.run()


def start_jobs():
    register_events(scheduler)
    scheduler.start()
