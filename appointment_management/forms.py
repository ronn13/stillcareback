from django import forms
from .models import Appointment, Seizure, Incident, Medication, BodyMap
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'assigned_staff': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time <= timezone.now():
            raise forms.ValidationError('Start time must be in the future.')
        return start_time

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        assigned_staff = cleaned_data.get('assigned_staff')
        if start_time and end_time:
            if end_time <= start_time:
                self.add_error('end_time', 'End time must be after start time.')
        # Double-booking check
        if assigned_staff and start_time and end_time:
            qs = Appointment.objects.filter(assigned_staff=assigned_staff)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            overlap = qs.filter(
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()
            if overlap:
                raise forms.ValidationError('Warning: This staff member already has an appointment during this time!')
        return cleaned_data


class SeizureForm(forms.ModelForm):
    class Meta:
        model = Seizure
        fields = ['appointment', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'appointment', 'time', 'persons_involved', 'addresses_of_persons_involved',
            'incident_details', 'was_person_injured', 'person_injured', 'injury_details',
            'incident_classification', 'remediation_taken', 'incident_notifiable_riddor',
            'f2508_document', 'other_people_notified', 'additional_information', 'insurers_advised'
        ]
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'persons_involved': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'addresses_of_persons_involved': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'incident_details': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'injury_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'remediation_taken': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'other_people_notified': forms.TextInput(attrs={'class': 'form-control'}),
            'additional_information': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'incident_classification': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'was_person_injured': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_was_person_injured'}),
            'incident_notifiable_riddor': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_incident_notifiable_riddor'}),
            'insurers_advised': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        was_person_injured = cleaned_data.get('was_person_injured')
        person_injured = cleaned_data.get('person_injured')
        injury_details = cleaned_data.get('injury_details')
        incident_notifiable_riddor = cleaned_data.get('incident_notifiable_riddor')
        f2508_document = cleaned_data.get('f2508_document')
        
        if was_person_injured:
            if not person_injured:
                raise forms.ValidationError("Person injured must be specified if someone was injured.")
            if not injury_details:
                raise forms.ValidationError("Injury details must be provided if someone was injured.")
        
        if incident_notifiable_riddor and not f2508_document:
            raise forms.ValidationError("F2508 document is required if incident is RIDDOR notifiable.")
        
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial required state based on current value
        if self.instance.pk and self.instance.was_person_injured:
            self.fields['person_injured'].required = True
            self.fields['injury_details'].required = True
        else:
            self.fields['person_injured'].required = False
            self.fields['injury_details'].required = False
            
        if self.instance.pk and self.instance.incident_notifiable_riddor:
            self.fields['f2508_document'].required = True
        else:
            self.fields['f2508_document'].required = False

    class Media:
        js = ('js/incident_form.js',)


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = [
            'appointment', 'name', 'strength', 'dose', 'frequency', 
            'administration_times', 'route', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'strength': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'dose': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'administration_times': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'route': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        strength = cleaned_data.get('strength')
        dose = cleaned_data.get('dose')
        
        if strength and dose and dose > strength:
            raise forms.ValidationError("Dose cannot be greater than the medication strength.")
        
        return cleaned_data


class BodyMapForm(forms.ModelForm):
    class Meta:
        model = BodyMap
        fields = [
            'appointment', 'practitioner', 'body_regions', 'injuries',
            'consent_given', 'consent_type', 'consent_notes',
            'photography_consent', 'photos_taken', 'photo_documentation',
            'medical_referral', 'medical_referral_details',
            'police_notified', 'police_notification_details',
            'safeguarding_referral', 'safeguarding_referral_details',
            'notes', 'follow_up_required', 'follow_up_details'
        ]
        widgets = {
            'practitioner': forms.Select(attrs={'class': 'form-control'}),
            'consent_notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'photo_documentation': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'medical_referral_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'police_notification_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'safeguarding_referral_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'follow_up_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'consent_given': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_consent_given'}),
            'photography_consent': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_photography_consent'}),
            'photos_taken': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_photos_taken'}),
            'medical_referral': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_medical_referral'}),
            'police_notified': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_police_notified'}),
            'safeguarding_referral': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_safeguarding_referral'}),
            'follow_up_required': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_follow_up_required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        consent_given = cleaned_data.get('consent_given')
        consent_type = cleaned_data.get('consent_type')
        photography_consent = cleaned_data.get('photography_consent')
        photos_taken = cleaned_data.get('photos_taken')
        
        if consent_given and not consent_type:
            raise forms.ValidationError("Consent type must be specified if consent was given.")
        
        if photos_taken and not photography_consent:
            raise forms.ValidationError("Photography consent is required if photos were taken.")
        
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial required state based on current value
        if self.instance.pk and self.instance.consent_given:
            self.fields['consent_type'].required = True
        else:
            self.fields['consent_type'].required = False
            
        if self.instance.pk and self.instance.photos_taken:
            self.fields['photography_consent'].required = True
        else:
            self.fields['photography_consent'].required = False

    class Media:
        js = ('js/body_map_form.js',)
