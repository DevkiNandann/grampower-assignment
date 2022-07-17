from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# set the default django settings for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery("main")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    broker_url="redis://{}:{}".format(
        settings.CELERY_ELASTIC_CACHE_URL, settings.CELERY_ELASTIC_CACHE_PORT
    )
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
