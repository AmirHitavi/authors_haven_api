import os

from celery import Celery

# TODO: change this in production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
