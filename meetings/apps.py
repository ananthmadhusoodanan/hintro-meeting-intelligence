from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meetings'

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN') != 'true':
            from meetings.scheduler import start_scheduler
            start_scheduler()
