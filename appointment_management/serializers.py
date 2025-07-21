from rest_framework import serializers
from .models import Appointment, Seizure, Incident, Medication, BodyMap
from client_management.models import Client
from client_management.serializers import ClientSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.full_name')
    client_location = serializers.ReadOnlyField(source='client.full_address')
    assigned_staff_name = serializers.ReadOnlyField(source='assigned_staff.user.username')
    duration_minutes = serializers.ReadOnlyField()
    available_checklist_items = serializers.ReadOnlyField()
    checklist_completion_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'title', 'description', 'start_time', 'end_time', 'status',
            'client', 'client_name', 'client_location', 'frequency', 'assigned_staff', 'assigned_staff_name',
            'actual_start_time', 'actual_end_time', 'checklist_items',
            'duration_minutes', 'available_checklist_items', 'checklist_completion_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        client_id = validated_data.pop('client_id')
        try:
            validated_data['client'] = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Client not found")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        client_id = validated_data.pop('client_id', None)
        if client_id:
            try:
                validated_data['client'] = Client.objects.get(id=client_id)
            except Client.DoesNotExist:
                raise serializers.ValidationError("Client not found")
        return super().update(instance, validated_data)


class SeizureSerializer(serializers.ModelSerializer):
    appointment_title = serializers.ReadOnlyField(source='appointment.title')
    client_name = serializers.ReadOnlyField(source='appointment.client.full_name')
    duration_minutes = serializers.ReadOnlyField()
    
    class Meta:
        model = Seizure
        fields = [
            'id', 'appointment', 'appointment_title', 'client_name',
            'start_time', 'end_time', 'duration_minutes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")
        
        return data


class IncidentSerializer(serializers.ModelSerializer):
    appointment_title = serializers.ReadOnlyField(source='appointment.title')
    client_name = serializers.ReadOnlyField(source='appointment.client.full_name')
    person_injured_display = serializers.ReadOnlyField(source='get_person_injured_display')
    
    class Meta:
        model = Incident
        fields = [
            'id', 'appointment', 'appointment_title', 'client_name',
            'time', 'persons_involved', 'addresses_of_persons_involved',
            'incident_details', 'was_person_injured', 'person_injured', 'person_injured_display',
            'injury_details', 'incident_classification', 'remediation_taken',
            'incident_notifiable_riddor', 'f2508_document', 'other_people_notified',
            'additional_information', 'insurers_advised', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        was_person_injured = data.get('was_person_injured')
        person_injured = data.get('person_injured')
        injury_details = data.get('injury_details')
        incident_notifiable_riddor = data.get('incident_notifiable_riddor')
        f2508_document = data.get('f2508_document')
        
        if was_person_injured:
            if not person_injured:
                raise serializers.ValidationError("Person injured must be specified if someone was injured.")
            if not injury_details:
                raise serializers.ValidationError("Injury details must be provided if someone was injured.")
        
        if incident_notifiable_riddor and not f2508_document:
            raise serializers.ValidationError("F2508 document is required if incident is RIDDOR notifiable.")
        
        return data


class MedicationSerializer(serializers.ModelSerializer):
    appointment_title = serializers.ReadOnlyField(source='appointment.title')
    client_name = serializers.ReadOnlyField(source='appointment.client.full_name')
    frequency_display = serializers.ReadOnlyField(source='get_frequency_display')
    route_display = serializers.ReadOnlyField(source='get_route_display')
    total_daily_dose = serializers.ReadOnlyField()
    
    class Meta:
        model = Medication
        fields = [
            'id', 'appointment', 'appointment_title', 'client_name',
            'name', 'strength', 'dose', 'frequency', 'frequency_display',
            'administration_times', 'route', 'route_display', 'notes',
            'total_daily_dose', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        strength = data.get('strength')
        dose = data.get('dose')
        
        if strength and dose and dose > strength:
            raise serializers.ValidationError("Dose cannot be greater than the medication strength.")
        
        return data


class BodyMapSerializer(serializers.ModelSerializer):
    appointment_title = serializers.ReadOnlyField(source='appointment.title')
    client_name = serializers.ReadOnlyField(source='appointment.client.full_name')
    practitioner_name = serializers.ReadOnlyField(source='practitioner.user.username')
    consent_type_display = serializers.ReadOnlyField(source='get_consent_type_display')
    injury_count = serializers.ReadOnlyField()
    has_serious_injuries = serializers.ReadOnlyField()
    
    class Meta:
        model = BodyMap
        fields = [
            'id', 'appointment', 'appointment_title', 'client_name',
            'date_recorded', 'practitioner', 'practitioner_name',
            'body_regions', 'injuries', 'injury_count', 'has_serious_injuries',
            'consent_given', 'consent_type', 'consent_type_display', 'consent_notes',
            'photography_consent', 'photos_taken', 'photo_documentation',
            'medical_referral', 'medical_referral_details',
            'police_notified', 'police_notification_details',
            'safeguarding_referral', 'safeguarding_referral_details',
            'notes', 'follow_up_required', 'follow_up_details',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'date_recorded', 'created_at', 'updated_at']

    def validate(self, data):
        consent_given = data.get('consent_given')
        consent_type = data.get('consent_type')
        photography_consent = data.get('photography_consent')
        photos_taken = data.get('photos_taken')
        
        if consent_given and not consent_type:
            raise serializers.ValidationError("Consent type must be specified if consent was given.")
        
        if photos_taken and not photography_consent:
            raise serializers.ValidationError("Photography consent is required if photos were taken.")
        
        return data
