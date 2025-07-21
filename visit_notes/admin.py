from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'appointment_info', 'uploaded_by', 'created_at', 'document_link')
    search_fields = ('appointment__title', 'appointment__client__first_name', 'appointment__client__last_name', 'uploaded_by__user__username', 'content')
    list_filter = ('uploaded_by', 'created_at', 'appointment')
    readonly_fields = ('created_at', 'updated_at', 'document_link')

    def appointment_info(self, obj):
        if obj.appointment:
            client = obj.appointment.client.full_name if hasattr(obj.appointment.client, 'full_name') else str(obj.appointment.client)
            return f"{obj.appointment.title} ({client})"
        return "-"
    appointment_info.short_description = 'Appointment'

    def document_link(self, obj):
        if obj.document:
            return f'<a href="{obj.document.url}" target="_blank">Download</a>'
        return "-"
    document_link.short_description = 'Document'
    document_link.allow_tags = True 