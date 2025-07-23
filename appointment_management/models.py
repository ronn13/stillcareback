from django.db import models
from django.conf import settings

# Create your models here.

class Appointment(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(help_text="When the appointment/visit should start")
    end_time = models.DateTimeField(help_text="When the appointment/visit should end")
    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ], default='scheduled')
    
    # Relationship to client
    client = models.ForeignKey(
        'client_management.Client',
        on_delete=models.CASCADE,
        related_name='appointments',
        help_text="The client this appointment is for"
    )
    
    # Recurring appointment fields
    frequency = models.CharField(
        max_length=20, 
        choices=FREQUENCY_CHOICES, 
        blank=True, 
        null=True,
        help_text="How often this appointment repeats"
    )
    
    assigned_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, blank=False, related_name='appointments', help_text="Staff member assigned to this appointment")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    VISIT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    status = models.CharField(
        max_length=20, 
        choices=VISIT_STATUS_CHOICES,
        default='scheduled'
    )
    
    # Actual visit timing
    actual_start_time = models.DateTimeField(blank=True, null=True)
    actual_end_time = models.DateTimeField(blank=True, null=True)
    
    # Visit checklist - completed items from client's care checklist
    checklist_items = models.JSONField(
        default=list,
        help_text="List of checklist items from the client's care plan"
    )
    
    @property
    def duration_minutes(self):
        """Calculate actual visit duration in minutes from appointment end time and visit end time"""
        if self.actual_end_time and self.appointment.end_time:
            # Use the earlier of the two end times
            end_time = min(self.actual_end_time, self.end_time)
            start_time = self.actual_start_time or self.start_time
            if start_time:
                duration = end_time - start_time
                return int(duration.total_seconds() / 60)
        return None

    @property
    def available_checklist_items(self):
        """Get the client's care checklist items that can be completed"""
        return self.client.care_checklist if self.client else []

    @property
    def checklist_completion_percentage(self):
        """Calculate the percentage of client checklist items completed"""
        if not self.available_checklist_items:
            return 0
        completed_count = len(self.checklist_items)
        total_count = len(self.available_checklist_items)
        return (completed_count / total_count) * 100 if total_count > 0 else 0

    def __str__(self):
        return f"{self.title} - {self.client.full_name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Seizure(models.Model):
    start_time = models.DateTimeField(help_text="When the seizure started")
    end_time = models.DateTimeField(blank=True, null=True, help_text="When the seizure ended")
    appointment = models.ForeignKey(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name='seizures',
        help_text="The appointment during which this seizure occurred"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Seizure"
        verbose_name_plural = "Seizures"
        ordering = ['-start_time']

    @property
    def duration_minutes(self):
        """Calculate seizure duration in minutes"""
        if self.end_time and self.start_time:
            duration = self.end_time - self.start_time
            return int(duration.total_seconds() / 60)
        return None

    def __str__(self):
        return f"Seizure for {self.appointment.client.full_name} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class Incident(models.Model):
    PERSON_INJURED_CHOICES = [
        ('service_user', 'Service User'),
        ('carer', 'Carer'),
        ('visitor', 'Visitor'),
        ('other', 'Other'),
    ]
    
    INCIDENT_CLASSIFICATION_CHOICES = [
        ('minor_injury', 'Minor Injury'),
        ('major_injury', 'Major Injury'),
        ('injury_3_days_sick_leave', 'Injury Required More Than 3 Days Sick Leave'),
        ('admitted_hospital', 'Admitted or Taken to Hospital'),
        ('fatality', 'Fatality'),
        ('self_harm_overdose', 'Self Harm (Overdose)'),
        ('self_harm_other', 'Self Harm (Other)'),
        ('verbal_abuse', 'Verbal Abuse'),
        ('physical_abuse', 'Physical Abuse'),
        ('assault', 'Assault'),
        ('arson', 'Arson'),
        ('damage_theft_property', 'Damage to/Theft of Property'),
        ('substance_misuse', 'Substance Misuse'),
        ('other', 'Other'),
    ]
    
    time = models.DateTimeField(help_text="When the incident occurred")
    persons_involved = models.TextField(help_text="Names and roles of persons involved in the incident")
    addresses_of_persons_involved = models.TextField(help_text="Addresses of persons involved")
    incident_details = models.TextField(help_text="Detailed description of what happened")
    was_person_injured = models.BooleanField(default=False, help_text="Was anyone injured in this incident?")
    injury_details = models.TextField(blank=True, null=True, help_text="Details of injuries sustained")
    person_injured = models.CharField(
        max_length=20,
        choices=PERSON_INJURED_CHOICES,
        blank=True,
        null=True,
        help_text="Who was injured (if applicable)"
    )
    incident_classification = models.JSONField(
        default=list,
        help_text="Classification of the incident (multiple selections allowed)"
    )
    remediation_taken = models.TextField(help_text="Actions taken to address the incident")
    incident_notifiable_riddor = models.BooleanField(
        default=False, 
        help_text="Is this incident notifiable under RIDDOR 1995?"
    )
    f2508_document = models.FileField(
        upload_to='incidents/f2508_documents/',
        blank=True,
        null=True,
        help_text="F2508 document (required if RIDDOR notifiable)"
    )
    other_people_notified = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Other people/organizations notified about this incident"
    )
    additional_information = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional information about the incident"
    )
    insurers_advised = models.BooleanField(
        default=False,
        help_text="Have insurers been advised of this incident?"
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='incidents',
        help_text="The appointment during which this incident occurred"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        ordering = ['-time']

    def __str__(self):
        return f"Incident for {self.appointment.client.full_name} on {self.time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.was_person_injured:
            if not self.person_injured:
                raise ValidationError("Person injured must be specified if someone was injured.")
            if not self.injury_details:
                raise ValidationError("Injury details must be provided if someone was injured.")
        if self.incident_notifiable_riddor and not self.f2508_document:
            raise ValidationError("F2508 document is required if incident is RIDDOR notifiable.")


class Medication(models.Model):
    FREQUENCY_CHOICES = [
        ('once_daily', 'Once Daily'),
        ('twice_daily', 'Twice Daily'),
        ('three_times_daily', 'Three Times Daily'),
        ('four_times_daily', 'Four Times Daily'),
        ('every_4_hours', 'Every 4 Hours'),
        ('every_6_hours', 'Every 6 Hours'),
        ('every_8_hours', 'Every 8 Hours'),
        ('every_12_hours', 'Every 12 Hours'),
        ('as_needed', 'As Needed (PRN)'),
        ('before_meals', 'Before Meals'),
        ('after_meals', 'After Meals'),
        ('with_meals', 'With Meals'),
        ('at_bedtime', 'At Bedtime'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('other', 'Other'),
    ]
    
    ADMINISTRATION_TIME_CHOICES = [
        ('morning', 'Morning (8:00 AM)'),
        ('mid_morning', 'Mid-Morning (10:00 AM)'),
        ('noon', 'Noon (12:00 PM)'),
        ('afternoon', 'Afternoon (2:00 PM)'),
        ('evening', 'Evening (6:00 PM)'),
        ('night', 'Night (8:00 PM)'),
        ('bedtime', 'Bedtime (10:00 PM)'),
        ('before_breakfast', 'Before Breakfast'),
        ('after_breakfast', 'After Breakfast'),
        ('before_lunch', 'Before Lunch'),
        ('after_lunch', 'After Lunch'),
        ('before_dinner', 'Before Dinner'),
        ('after_dinner', 'After Dinner'),
        ('as_needed', 'As Needed'),
        ('other', 'Other'),
    ]
    
    ROUTE_CHOICES = [
        ('oral', 'Oral'),
        ('buccal', 'Buccal'),
        ('sublingual', 'Sublingual'),
        ('intravenous', 'Intravenous (IV)'),
        ('intramuscular', 'Intramuscular (IM)'),
        ('subcutaneous', 'Subcutaneous (SC)'),
        ('topical', 'Topical'),
        ('inhalation', 'Inhalation'),
        ('nasal', 'Nasal'),
        ('ophthalmic', 'Ophthalmic (Eye)'),
        ('otic', 'Otic (Ear)'),
        ('rectal', 'Rectal'),
        ('transdermal', 'Transdermal'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200, help_text="Name of the medication")
    strength = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Strength of the medication in mg"
    )
    dose = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Dose to be administered in mg"
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        help_text="How often the medication should be administered"
    )
    administration_times = models.JSONField(
        default=list,
        help_text="Specific times when medication should be administered (multiple selections allowed)"
    )
    route = models.CharField(
        max_length=20,
        choices=ROUTE_CHOICES,
        help_text="Route of administration"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the medication administration"
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='medications',
        help_text="The appointment during which this medication is administered"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Medication"
        verbose_name_plural = "Medications"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} {self.strength}mg - {self.dose}mg {self.get_frequency_display()} for {self.appointment.client.full_name}"

    @property
    def total_daily_dose(self):
        """Calculate total daily dose based on frequency and dose"""
        frequency_mapping = {
            'once_daily': 1,
            'twice_daily': 2,
            'three_times_daily': 3,
            'four_times_daily': 4,
            'every_4_hours': 6,  # 24/4 = 6 times
            'every_6_hours': 4,  # 24/6 = 4 times
            'every_8_hours': 3,  # 24/8 = 3 times
            'every_12_hours': 2,  # 24/12 = 2 times
            'as_needed': 0,  # Variable
            'before_meals': 3,  # Assuming 3 meals
            'after_meals': 3,   # Assuming 3 meals
            'with_meals': 3,    # Assuming 3 meals
            'at_bedtime': 1,
            'weekly': 1/7,      # Once per week
            'monthly': 1/30,    # Once per month
            'other': 0,         # Unknown
        }
        
        times_per_day = frequency_mapping.get(self.frequency, 0)
        return self.dose * times_per_day if times_per_day > 0 else None


class BodyMap(models.Model):
    INJURY_TYPE_CHOICES = [
        ('pressure_ulcer', 'Pressure Ulcer'),
        ('cut', 'Cut/Laceration'),
        ('abrasion', 'Abrasion/Scrape'),
        ('burn', 'Burn'),
        ('swelling', 'Swelling'),
        ('redness', 'Redness'),
        ('scar', 'Scar'),
        ('tenderness', 'Tenderness'),
        ('bruise', 'Bruise'),
        ('other', 'Other'),
    ]
    
    INJURY_COLOR_CHOICES = [
        ('red', 'Red'),
        ('purple', 'Purple'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('brown', 'Brown'),
        ('black', 'Black'),
        ('pink', 'Pink'),
        ('white', 'White'),
        ('other', 'Other'),
    ]
    
    HEALING_STAGE_CHOICES = [
        ('fresh', 'Fresh (0-24 hours)'),
        ('early', 'Early Healing (1-3 days)'),
        ('intermediate', 'Intermediate (3-7 days)'),
        ('late', 'Late Healing (1-2 weeks)'),
        ('healed', 'Healed'),
        ('unknown', 'Unknown'),
    ]
    
    CONSENT_TYPE_CHOICES = [
        ('verbal', 'Verbal Consent'),
        ('written', 'Written Consent'),
        ('implied', 'Implied Consent'),
        ('emergency', 'Emergency Treatment'),
        ('guardian', 'Guardian Consent'),
        ('none', 'No Consent Given'),
    ]
    
    # Basic Information
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='body_maps',
        help_text="The appointment during which this body map was recorded"
    )
    date_recorded = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the body map was recorded"
    )
    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='body_maps_recorded',
        help_text="Healthcare practitioner who recorded the body map"
    )
    
    # Body Map Data - JSON structure for front/back body regions
    body_regions = models.JSONField(
        default=dict,
        help_text="Body regions with injury markings (front/back views)"
    )
    
    # Injury Details - Detailed injury records
    injuries = models.JSONField(
        default=list,
        help_text="Detailed injury records with location, size, type, color, etc."
    )
    
    # Documentation and Consent
    consent_given = models.BooleanField(
        default=False,
        help_text="Was consent given for the body map examination?"
    )
    consent_type = models.CharField(
        max_length=20,
        choices=CONSENT_TYPE_CHOICES,
        blank=True,
        null=True,
        help_text="Type of consent obtained"
    )
    consent_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Notes about consent process"
    )
    
    # Photography Documentation
    photography_consent = models.BooleanField(
        default=False,
        help_text="Was consent given for photography?"
    )
    photos_taken = models.BooleanField(
        default=False,
        help_text="Were photographs taken?"
    )
    photo_documentation = models.TextField(
        blank=True,
        null=True,
        help_text="Details of photographs taken"
    )
    
    # Referrals and Notifications
    medical_referral = models.BooleanField(
        default=False,
        help_text="Was a medical referral made?"
    )
    medical_referral_details = models.TextField(
        blank=True,
        null=True,
        help_text="Details of medical referral"
    )
    police_notified = models.BooleanField(
        default=False,
        help_text="Were the police notified?"
    )
    police_notification_details = models.TextField(
        blank=True,
        null=True,
        help_text="Details of police notification"
    )
    safeguarding_referral = models.BooleanField(
        default=False,
        help_text="Was a safeguarding referral made?"
    )
    safeguarding_referral_details = models.TextField(
        blank=True,
        null=True,
        help_text="Details of safeguarding referral"
    )
    
    # Additional Information
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Additional notes about the body map examination"
    )
    follow_up_required = models.BooleanField(
        default=False,
        help_text="Is follow-up required?"
    )
    follow_up_details = models.TextField(
        blank=True,
        null=True,
        help_text="Details of required follow-up"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Body Map"
        verbose_name_plural = "Body Maps"
        ordering = ['-date_recorded']

    def __str__(self):
        return f"Body Map for {self.appointment.client.full_name} on {self.date_recorded.strftime('%Y-%m-%d %H:%M')}"

    @property
    def injury_count(self):
        """Count the total number of injuries recorded"""
        return len(self.injuries) if self.injuries else 0

    @property
    def has_serious_injuries(self):
        """Check if any injuries are marked as serious"""
        if not self.injuries:
            return False
        for injury in self.injuries:
            if injury.get('serious', False):
                return True
        return False

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.consent_given and not self.consent_type:
            raise ValidationError("Consent type must be specified if consent was given.")
        if self.photos_taken and not self.photography_consent:
            raise ValidationError("Photography consent is required if photos were taken.")


class VisitLocationLog(models.Model):
    LOG_TYPE_CHOICES = [
        ('start', 'Start'),
        ('end', 'End'),
        ('deviation', 'Deviation'),
    ]
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='location_logs')
    log_type = models.CharField(max_length=10, choices=LOG_TYPE_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    distance_from_client = models.FloatField(help_text='Distance from client residence in meters')

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.get_log_type_display()} log for {self.appointment} at {self.timestamp}"
