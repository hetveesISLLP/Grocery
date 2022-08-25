import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for current project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GS.settings')
# Instantiate Celery, pass the project name in Celery(project_name)
app = Celery('GS')

# Using a string here means the worker doesn't have to serialize configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
# load celery configuration values from the settings object from django.conf
# We used namespace="CELERY" to prevent clashes with other Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings
# app.conf.beat_schedule = {
#     'send_mail_if_available_everyday': {
#         'task': 'product.tasks.send_email_when_quantity_available',
#         'schedule': crontab(minute=0, hour=0),
#     },
# }
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata")

# Load task modules from all registered Django apps.
# tells Celery to look for Celery tasks from applications defined in settings.INSTALLED_APPS
app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
