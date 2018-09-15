from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youzan.settings')

app = Celery("youzan")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("name is ....")

# celery -A youzan worker -l info -P eventlet


from kombu import Exchange, Queue

default_exchange = Exchange('default', type='direct')
media_exchange = Exchange('media', type='direct')
app.conf.task_queues = {
    Queue('default', default_exchange, routing_key='default'),
    Queue('video', media_exchange, routing_key='media.video'),
    Queue('image', media_exchange, routing_key='media.image')
}
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'