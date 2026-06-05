from django.apps import AppConfig


class MeetingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meetings'

    def ready(self):
        import os
        # Only start in main process AND only when server is running (not during build/migrate)
        if os.environ.get('RUN_MAIN') != 'true' and os.environ.get('RENDER'):
            return
        if os.environ.get('RUN_MAIN') == 'true':
            from meetings.scheduler import start_scheduler
            start_scheduler()