from django.db import models
from django.conf import settings
from appointment_management.models import Appointment

class Note(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField(blank=True)
    document = models.FileField(upload_to='visit_notes/documents/', blank=True, null=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='uploaded_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for Appointment {self.appointment.id} by {self.uploaded_by} on {self.created_at.strftime('%Y-%m-%d %H:%M')}" 