import os
import django
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eco_app_back.settings")
django.setup()
app = Celery("eco_app_back")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.broker_url = 'memory://'
app.conf.result_backend = 'rpc://'
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'eco.tasks.add',
        'schedule': 30.0,
        'args': (16, 16),
    }
}