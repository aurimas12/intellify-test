import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Optimize by using a string for configuration without serialization in child processes and set 'celery' namespace for celery-related keys
app.config_from_object('django.conf:settings',
                       namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()

# celery beat tasks
app.conf.beat_shedule = {
    'send-data-every-5-minutes': {
        'task': 'users.tasks.test',
        'schedule': crontab(minute='*/5')
    }
}
