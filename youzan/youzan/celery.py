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


# 多路由处理不同的任务
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

# 调用任务时,不但需要传参并且对任务的重试次数已经重试间隔时间有其他要求的时候,delay()已经不适用了,需要用apply_async()的方式进行处理
# 例如,现在需要将task中的add函数进行异步引用操作
from interapp.tasks import add

# 注意在传参数的时候不能像delay()一样直接进行传参,需要将位置参数放进[ ]列表中  关键字参数放进{ }字典中
# 这样是为了区别于后面的设置参数
add.apply_async([1, 3, 4], {"token": 123}, retry=True, retry_policy={
    # 最大的重试次数
    'max_retries': 3,
    # 定义首次重试间隔的秒数
    'interval_start': 0,
    # 每进行一次重试,延迟的时间长度
    'interval_step': 0.2,
    # 重试之间间隔的最大秒数
    'interval_max': 0.2,
})
