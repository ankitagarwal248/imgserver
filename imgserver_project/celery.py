from __future__ import absolute_import
import os
import re

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imgserver_project.settings')
app = Celery('imgserver_project',
             broker='redis://localhost:6379',
             backend='redis://localhost:6379'
             )

# app = Celery('imgserver_project',
#              broker='amqp://jimmy:jimmy123@localhost/jimmy_vhost',
#              backend='rpc://',
#              )

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_routes = {
    'master.tasks.dummy_task': {'queue': 'feeds'},
    'master.tasks.dummy_data': {'queue': 'filter'}
}



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))