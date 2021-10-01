from celery import Celery
try:
    celery_app = Celery("worker", broker="amqp://guest@queue//")

    celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
except:
    pass
