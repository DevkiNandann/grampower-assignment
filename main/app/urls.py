from django.urls import path
from app.views import (
    Login,
    MeterView
)
from .bg_task import RunBackgroundTasks

task = RunBackgroundTasks()

if task.is_running_as_server:
    task.runtask()
    

urlpatterns = [
    path("", Login.as_view(), name="login"),
    path("meter", MeterView.as_view(), name="meter-list"),
    path("meter/<id>", MeterView.as_view(), name="meter-detail")
]
