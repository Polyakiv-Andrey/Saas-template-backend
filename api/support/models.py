from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SupportTicket(models.Model):
    TICKET_STATUSES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.FileField(upload_to='support_tickets/%Y/%m/%d/', blank=True, null=True,)
    status = models.CharField(
        max_length=20,
        choices=TICKET_STATUSES,
        default='open'
    )
    created_by = models.EmailField(default="anonim@n.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    reported_by = models.ForeignKey(
        User,
        related_name='reported_tickets',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"Ticket {self.id} - {self.title}"
