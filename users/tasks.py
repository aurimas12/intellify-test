import random

from celery import shared_task
from core.celery import app

from users.models import TimeSeries


@shared_task
def add(x, y):
    return x + y


@app.task
def generate_data(is_authenticated):
    if is_authenticated:
        value = random.gauss(1.0, 10.0)
        TimeSeries.objects.create(data=value).save()
    return True
