from django.apps import AppConfig
from .bg_task import RunBackgroundTasks
import sys


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self, *args, **kwargs):
        is_manage_py = any(arg.casefold().endswith("manage.py") for arg in sys.argv)
        is_runserver = any(arg.casefold() == "runserver" for arg in sys.argv)

        if (is_manage_py and is_runserver) or (not is_manage_py):
            RunBackgroundTasks.is_running_as_server = True
