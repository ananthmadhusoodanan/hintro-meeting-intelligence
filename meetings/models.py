from django.db import models


class Meeting(models.Model):
    # CharField = text with a max length (maps to VARCHAR in SQL)
    title = models.CharField(max_length=255)

    # JSONField = stores a list or dict as JSON (PostgreSQL supports this natively)
    # This stores the participants list: ["alice@example.com", "bob@example.com"]
    participants = models.JSONField(default=list)

    # DateTimeField = stores date + time
    meeting_date = models.DateTimeField()

    # transcript stores the array of {timestamp, speaker, text} objects
    transcript = models.JSONField(default=list)

    # analysis stores the AI-generated output after /analyze is called
    # null=True means this column can be empty (meeting starts with no analysis)
    analysis = models.JSONField(null=True, blank=True)

    # auto_now_add=True means Django sets this automatically when record is created
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # This controls the SQL table name (default would be meetings_meeting)
        db_table = 'meetings'
        ordering = ['-created_at']  # newest first by default

    def __str__(self):
        # This is what shows in Django admin and debug output
        return f"{self.title} ({self.meeting_date.date()})"