from django.db import models
from meetings.models import Meeting


class ActionItem(models.Model):
    # Status choices — like an enum
    # First value is stored in DB, second is human-readable label
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    # ForeignKey = a relationship to another table
    # If a Meeting is deleted, delete its action items too (CASCADE)
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='action_items'  # lets us do meeting.action_items.all()
    )

    task = models.TextField()  # TextField = unlimited length text
    assignee = models.EmailField()  # EmailField = validates email format

    due_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    # Citations linking this action item back to transcript segments
    citations = models.JSONField(default=list)

    # Reminder tracking
    reminder_sent = models.BooleanField(default=False)
    last_reminded_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'action_items'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.task} → {self.assignee} [{self.status}]"