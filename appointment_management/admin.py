from django.contrib import admin
from .models import Appointment, Seizure, Incident, Medication, BodyMap

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'client', 
        'start_time', 
        'end_time', 
        'status', 
        'frequency', 
        'assigned_staff',
        'checklist_completion_display',
        'duration_minutes',
        'created_at'
    ]
    list_filter = [
        'status', 
        'frequency', 
        'assigned_staff',
        'start_time', 
        'created_at'
    ]
    search_fields = [
        'title', 
        'description', 
        'client__first_name', 
        'client__last_name',
        'assigned_staff__user__username'
    ]
    readonly_fields = ['created_at', 'updated_at', 'duration_minutes', 'checklist_completion_percentage', 'available_checklist_items']
    fieldsets = (
        ('Appointment Details', {
            'fields': ('title', 'description', 'client', 'start_time', 'end_time', 'status', 'assigned_staff')
        }),
        ('Recurring Settings', {
            'fields': ('frequency',),
            'classes': ('collapse',)
        }),
        ('Checklist & Care', {
            'fields': ('checklist_items', 'available_checklist_items', 'checklist_completion_percentage')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'duration_minutes'),
            'classes': ('collapse',)
        }),
    )

    def checklist_completion_display(self, obj):
        percentage = obj.checklist_completion_percentage
        return f"{percentage:.1f}%"
    checklist_completion_display.short_description = 'Checklist %'


@admin.register(Seizure)
class SeizureAdmin(admin.ModelAdmin):
    list_display = [
        'appointment_client',
        'start_time',
        'end_time',
        'duration_minutes',
        'appointment_title',
        'created_at'
    ]
    list_filter = [
        'start_time',
        'created_at',
        'appointment__status'
    ]
    search_fields = [
        'appointment__client__first_name',
        'appointment__client__last_name',
        'appointment__title'
    ]
    readonly_fields = ['created_at', 'updated_at', 'duration_minutes']
    fieldsets = (
        ('Seizure Details', {
            'fields': ('appointment', 'start_time', 'end_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'duration_minutes'),
            'classes': ('collapse',)
        }),
    )

    def appointment_client(self, obj):
        return obj.appointment.client.full_name if obj.appointment and obj.appointment.client else '-'
    appointment_client.short_description = 'Client'

    def appointment_title(self, obj):
        return obj.appointment.title if obj.appointment else '-'
    appointment_title.short_description = 'Appointment'


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = [
        'appointment_client',
        'time',
        'was_person_injured',
        'person_injured_display',
        'incident_classification_display',
        'incident_notifiable_riddor',
        'insurers_advised',
        'created_at'
    ]
    list_filter = [
        'time',
        'was_person_injured',
        'person_injured',
        'incident_notifiable_riddor',
        'insurers_advised',
        'created_at',
        'appointment__status'
    ]
    search_fields = [
        'appointment__client__first_name',
        'appointment__client__last_name',
        'appointment__title',
        'persons_involved',
        'incident_details'
    ]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Incident Details', {
            'fields': ('appointment', 'time', 'persons_involved', 'addresses_of_persons_involved', 'incident_details')
        }),
        ('Injury Information', {
            'fields': ('was_person_injured', 'person_injured', 'injury_details'),
            'classes': ('collapse',)
        }),
        ('Classification', {
            'fields': ('incident_classification',)
        }),
        ('Remediation & Actions', {
            'fields': ('remediation_taken',)
        }),
        ('Notifications', {
            'fields': ('incident_notifiable_riddor', 'f2508_document', 'other_people_notified', 'insurers_advised')
        }),
        ('Additional Information', {
            'fields': ('additional_information',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def appointment_client(self, obj):
        return obj.appointment.client.full_name if obj.appointment and obj.appointment.client else '-'
    appointment_client.short_description = 'Client'

    def person_injured_display(self, obj):
        if obj.was_person_injured and obj.person_injured:
            return obj.get_person_injured_display()
        return "No injury"
    person_injured_display.short_description = 'Person Injured'

    def incident_classification_display(self, obj):
        if obj.incident_classification:
            classifications = []
            for choice in obj.incident_classification:
                for code, label in obj.INCIDENT_CLASSIFICATION_CHOICES:
                    if code == choice:
                        classifications.append(label)
                        break
            return ', '.join(classifications[:2]) + ('...' if len(classifications) > 2 else '')
        return "None"
    incident_classification_display.short_description = 'Classification'

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = [
        'appointment_client',
        'name',
        'strength_display',
        'dose_display',
        'frequency_display',
        'administration_times_display',
        'route_display',
        'total_daily_dose_display',
        'created_at'
    ]
    list_filter = [
        'frequency',
        'route',
        'created_at',
        'appointment__status'
    ]
    search_fields = [
        'name',
        'appointment__client__first_name',
        'appointment__client__last_name',
        'appointment__title',
        'notes'
    ]
    readonly_fields = ['created_at', 'updated_at', 'total_daily_dose_display']
    fieldsets = (
        ('Medication Details', {
            'fields': ('appointment', 'name', 'strength', 'dose', 'frequency', 'route')
        }),
        ('Administration', {
            'fields': ('administration_times',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Calculations', {
            'fields': ('total_daily_dose_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def appointment_client(self, obj):
        return obj.appointment.client.full_name if obj.appointment and obj.appointment.client else '-'
    appointment_client.short_description = 'Client'

    def strength_display(self, obj):
        return f"{obj.strength}mg"
    strength_display.short_description = 'Strength'

    def dose_display(self, obj):
        return f"{obj.dose}mg"
    dose_display.short_description = 'Dose'

    def frequency_display(self, obj):
        return obj.get_frequency_display()
    frequency_display.short_description = 'Frequency'

    def administration_times_display(self, obj):
        if obj.administration_times:
            times = []
            for choice in obj.administration_times:
                for code, label in obj.ADMINISTRATION_TIME_CHOICES:
                    if code == choice:
                        times.append(label)
                        break
            return ', '.join(times[:2]) + ('...' if len(times) > 2 else '')
        return "None"
    administration_times_display.short_description = 'Administration Times'

    def route_display(self, obj):
        return obj.get_route_display()
    route_display.short_description = 'Route'

    def total_daily_dose_display(self, obj):
        total = obj.total_daily_dose
        if total is not None:
            return f"{total:.2f}mg"
        return "Variable"
    total_daily_dose_display.short_description = 'Total Daily Dose'


@admin.register(BodyMap)
class BodyMapAdmin(admin.ModelAdmin):
    list_display = [
        'appointment_client',
        'date_recorded',
        'practitioner_display',
        'injury_count_display',
        'consent_status',
        'photography_status',
        'referral_status',
        'follow_up_required',
        'created_at'
    ]
    list_filter = [
        'date_recorded',
        'consent_given',
        'photography_consent',
        'photos_taken',
        'medical_referral',
        'police_notified',
        'safeguarding_referral',
        'follow_up_required',
        'created_at',
        'appointment__status'
    ]
    search_fields = [
        'appointment__client__first_name',
        'appointment__client__last_name',
        'appointment__title',
        'practitioner__user__username',
        'notes',
        'consent_notes'
    ]
    readonly_fields = ['created_at', 'updated_at', 'injury_count_display', 'has_serious_injuries_display']
    fieldsets = (
        ('Basic Information', {
            'fields': ('appointment', 'date_recorded', 'practitioner')
        }),
        ('Body Map Data', {
            'fields': ('body_regions', 'injuries'),
            'classes': ('collapse',)
        }),
        ('Consent and Documentation', {
            'fields': ('consent_given', 'consent_type', 'consent_notes')
        }),
        ('Photography', {
            'fields': ('photography_consent', 'photos_taken', 'photo_documentation')
        }),
        ('Referrals and Notifications', {
            'fields': (
                'medical_referral', 'medical_referral_details',
                'police_notified', 'police_notification_details',
                'safeguarding_referral', 'safeguarding_referral_details'
            )
        }),
        ('Additional Information', {
            'fields': ('notes', 'follow_up_required', 'follow_up_details')
        }),
        ('Calculations', {
            'fields': ('injury_count_display', 'has_serious_injuries_display'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def appointment_client(self, obj):
        return obj.appointment.client.full_name if obj.appointment and obj.appointment.client else '-'
    appointment_client.short_description = 'Client'

    def practitioner_display(self, obj):
        return obj.practitioner.user.username if obj.practitioner and obj.practitioner.user else '-'
    practitioner_display.short_description = 'Practitioner'

    def injury_count_display(self, obj):
        count = obj.injury_count
        return f"{count} injury{'ies' if count != 1 else ''}"
    injury_count_display.short_description = 'Injury Count'

    def consent_status(self, obj):
        if obj.consent_given:
            return f"✓ {obj.get_consent_type_display()}" if obj.consent_type else "✓ Given"
        return "✗ Not Given"
    consent_status.short_description = 'Consent'

    def photography_status(self, obj):
        if obj.photos_taken:
            return "✓ Photos Taken"
        elif obj.photography_consent:
            return "✓ Consent Given"
        return "✗ No Photos"
    photography_status.short_description = 'Photography'

    def referral_status(self, obj):
        referrals = []
        if obj.medical_referral:
            referrals.append("Medical")
        if obj.police_notified:
            referrals.append("Police")
        if obj.safeguarding_referral:
            referrals.append("Safeguarding")
        return ", ".join(referrals) if referrals else "None"
    referral_status.short_description = 'Referrals'

    def has_serious_injuries_display(self, obj):
        return "Yes" if obj.has_serious_injuries else "No"
    has_serious_injuries_display.short_description = 'Serious Injuries'

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
