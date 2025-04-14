from celery import shared_task


@shared_task
def pong():
    print(['비자 정보', '문화 정보', '산업 정보'])
