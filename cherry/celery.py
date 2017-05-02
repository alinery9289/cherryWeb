from __future__ import absolute_import

from celery import Celery
from kombu import Queue, Exchange

from cherry.util.config import conf_dict

rabbit_user = conf_dict['rabbitmq']['user']
rabbit_password = conf_dict['rabbitmq']['password']
rabbit_host = conf_dict['rabbitmq']['ip']
rabbit_port = conf_dict['rabbitmq']['port']

broker = """amqp://%s:%s@%s:%s""" % \
    (rabbit_user, rabbit_password, rabbit_host, rabbit_port)
backend = """amqp://%s:%s@%s:%s""" % \
    (rabbit_user, rabbit_password, rabbit_host, rabbit_port)

celery_app = Celery('cherry',
                    broker = broker,
                    backend = backend,
                    include=['cherry.tasks.tasks','cherry.jobs.launch'])

# optional configurations, see the application user guide
celery_app.conf.update(
    CELERY_QUEUES = (
        Queue('cherry_task_group1', Exchange('task'), routing_key='cherry.task.group1'),
        Queue('cherry_job', Exchange('job'), routing_key='cherry.job'),
    ),
    CELERY_ROUTES = {
        "cherry.task.TemplateTranscoder": {"exchange": "task", "routing_key": "cherry.task.group1"},
        "cherry.task.SimpleTranscoder": {"exchange": "task", "routing_key": "cherry.task.group1"},
        "cherry.task.sliced_job":{"exchange": "job", "routing_key": "cherry.job"},
        "cherry.task.intact_job":{"exchange": "job", "routing_key": "cherry.job"},
    }

    # CELERY_DEFAULT_EXCHANGE = 'Cherry.TaskGroup_1',
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic',
    # CELERY_DEFAULT_ROUTING_KEY = 'Cherry.TaskGroup_1.#',
)

if __name__ == '__main__':
    celery_app.start()
