import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "daily-insight-collection": {
        "task": "insights.tasks.daily_insight_collection",
        "schedule": crontab(hour=0, minute=0),  # 매일 자정에 실행
        "args": (10,),  # 검색어 개수
    },
    "process_insights_to_structured_info": {
        "task": "insights.tasks.process_insights_to_structured_info",
        "schedule": crontab(day_of_week=1, hour=0, minute=0),  # 매주 월요일 자정에 실행
        "args": (),  # 인자 없음
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
