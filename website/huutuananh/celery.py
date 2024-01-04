# coding: utf-8
import os

from celery import Celery
from celery.schedules import crontab

from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "huutuananh.settings")
app = Celery("huutuananh")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="Asia/Ho_Chi_Minh",
    enable_utc=True,
)

app.autodiscover_tasks(related_name="bg_tasks")


@app.task(bind=True)
def backup_db(self):
    print("Chạy backup db")
    call_command("dbbackup", clean=True, quiet=True)
    # print(out.getvalue().strip().split("\n"))
    print("Xong backup db")


app.conf.beat_schedule = {
    # Backup vào thứ 2 hằng tuần
    "backup-every-week": {
        "task": "huutuananh.celery.backup_db",
        "schedule": crontab(hour=0, minute=0, day_of_week=1),
        # "schedule": 60,
        # "args": (16, 16),
    },
}
