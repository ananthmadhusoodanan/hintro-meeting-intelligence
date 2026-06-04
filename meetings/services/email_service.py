import os
import resend
import logging

logger = logging.getLogger(__name__)

resend.api_key = os.getenv('RESEND_API_KEY')


def send_reminder_email(assignee: str, task: str, due_date, meeting_title: str) -> bool:
    try:
        due_str = due_date.strftime('%Y-%m-%d %H:%M UTC') if due_date else 'No due date'
        params = {
            "from": os.getenv('RESEND_FROM_EMAIL', 'onboarding@resend.dev'),
            "to": [assignee],
            "subject": f"Reminder: {task}",
            "html": f"""
                <h2>Action Item Reminder</h2>
                <p>Meeting: <strong>{meeting_title}</strong></p>
                <table>
                    <tr><td><strong>Task:</strong></td><td>{task}</td></tr>
                    <tr><td><strong>Assigned To:</strong></td><td>{assignee}</td></tr>
                    <tr><td><strong>Due Date:</strong></td><td>{due_str}</td></tr>
                </table>
                <p>Please update the status as soon as possible.</p>
            """
        }
        email = resend.Emails.send(params)
        logger.info(f"Reminder sent to {assignee} — id: {email['id']}")
        return True
    except Exception as e:
        logger.error(f"Failed to send reminder to {assignee}: {str(e)}")
        return False
