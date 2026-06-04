import logging
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore

logger = logging.getLogger(__name__)
scheduler = None


def send_overdue_reminders():
    from action_items.models import ActionItem
    from meetings.services.email_service import send_reminder_email

    now = timezone.now()
    overdue_items = ActionItem.objects.filter(
        due_date__lt=now,
        reminder_sent=False
    ).exclude(status='COMPLETED').select_related('meeting')

    if not overdue_items.exists():
        logger.info("No overdue action items found.")
        return

    logger.info(f"Found {overdue_items.count()} overdue item(s). Sending reminders...")

    for item in overdue_items:
        success = send_reminder_email(
            assignee=item.assignee,
            task=item.task,
            due_date=item.due_date,
            meeting_title=item.meeting.title
        )
        if success:
            item.reminder_sent = True
            item.last_reminded_at = now
            item.save()


def start_scheduler():
    global scheduler
    if scheduler and scheduler.running:
        return

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        send_overdue_reminders,
        trigger=IntervalTrigger(minutes=5),
        id="send_overdue_reminders",
        name="Send overdue reminders",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started.")
