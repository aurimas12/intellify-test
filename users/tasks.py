
from celery import shared_task, Celery
from .models import Project, TimeSeries, UserAccount

from core.celery import app
import random


@shared_task
def add(x, y):
    return x + y


@app.task
def generate_data(email):
    if UserAccount.objects.get(email=email).is_authenticated:
        value = random.gauss(1.0, 10.0)
        TimeSeries.objects.create(data=value).save()
    return True
