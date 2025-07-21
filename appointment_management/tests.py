from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import json

from .models import Appointment, Seizure, Incident, Medication, BodyMap
from client_management.models import Client

User = get_user_model()


class VisitManagementAPITestCase(TestCase):
    """Test case for visit management API endpoints"""

    def setUp(self):
        """Set up test data"""
        # Create test user and staff
        self.user = User.objects.create_user(
            username='test_staff',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test client
        self.client_obj = Client.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Test St'
        )
        
        # Create test appointment
        self.appointment = Appointment.objects.create(
            title='Test Visit',
            description='Test appointment for API testing',
            client=self.client_obj,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=2),
            status='scheduled',
            assigned_staff=self.user # Changed from self.staff to self.user
        )
        
        # Create API client
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)

    def test_staff_dashboard(self):
        """Test staff dashboard endpoint"""
        url = '/appointments/api/staff/dashboard/'
        response = self.api_client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        # Check that dashboard data is returned
        self.assertIn('today_appointments', data)
        self.assertIn('in_progress_appointments', data)
        self.assertIn('upcoming_appointments', data)
        self.assertIn('recent_incidents', data)
        self.assertIn('recent_seizures', data)
        self.assertIn('stats', data)
        
        # Check stats
        stats = data['stats']
        self.assertIn('today_count', stats)
        self.assertIn('in_progress_count', stats)
        self.assertIn('upcoming_count', stats)

    def test_appointment_endpoints(self):
        """Test appointment management endpoints"""
        
        # Test get all appointments
        url = '/appointments/api/staff/appointments/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test get today's appointments
        url = '/appointments/api/staff/appointments/today/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test get upcoming appointments
        url = '/appointments/api/staff/appointments/upcoming/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test get in-progress appointments
        url = '/appointments/api/staff/appointments/in_progress/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test start visit
        url = f'/appointments/api/staff/appointments/{self.appointment.id}/start_visit/'
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('actual_start_time', data)
        self.assertEqual(data['message'], 'Visit started successfully')
        
        # Refresh appointment from database
        self.appointment.refresh_from_db()
        self.assertIsNotNone(self.appointment.actual_start_time)
        self.assertEqual(self.appointment.status, 'in_progress')
        
        # Test update checklist
        url = f'/appointments/api/staff/appointments/{self.appointment.id}/update_checklist/'
        checklist_data = {'checklist_items': ['medication', 'hygiene', 'breakfast']}
        response = self.api_client.post(url, checklist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('checklist_items', data)
        self.assertIn('completion_percentage', data)
        self.assertEqual(data['message'], 'Checklist updated successfully')
        
        # Test end visit
        url = f'/appointments/api/staff/appointments/{self.appointment.id}/end_visit/'
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('actual_end_time', data)
        self.assertIn('duration_minutes', data)
        self.assertEqual(data['message'], 'Visit ended successfully')
        
        # Refresh appointment from database
        self.appointment.refresh_from_db()
        self.assertIsNotNone(self.appointment.actual_end_time)
        self.assertEqual(self.appointment.status, 'completed')
        self.assertIsNotNone(self.appointment.duration_minutes)

    def test_seizure_endpoints(self):
        """Test seizure management endpoints"""
        
        # Test create seizure
        url = '/appointments/api/staff/seizures/'
        seizure_data = {
            'appointment': self.appointment.id,
            'start_time': timezone.now().isoformat()
        }
        response = self.api_client.post(url, seizure_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = response.json()
        self.assertIn('id', data)
        self.assertIn('appointment', data)
        self.assertIn('start_time', data)
        
        seizure_id = data['id']
        
        # Test get seizures
        url = '/appointments/api/staff/seizures/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test end seizure
        url = f'/appointments/api/staff/seizures/{seizure_id}/end_seizure/'
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('end_time', data)
        self.assertIn('duration_minutes', data)
        self.assertEqual(data['message'], 'Seizure ended successfully')

    def test_incident_endpoints(self):
        """Test incident management endpoints"""
        
        # Test create incident
        url = '/appointments/api/staff/incidents/'
        incident_data = {
            'appointment': self.appointment.id,
            'time': timezone.now().isoformat(),
            'persons_involved': 'John Doe, Jane Smith',
            'addresses_of_persons_involved': '123 Main St',
            'incident_details': 'Test incident for API testing',
            'was_person_injured': False,
            'incident_classification': ['other'],
            'remediation_taken': 'Documented incident',
            'incident_notifiable_riddor': False,
            'insurers_advised': False
        }
        response = self.api_client.post(url, incident_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = response.json()
        self.assertIn('id', data)
        self.assertIn('appointment', data)
        self.assertIn('time', data)
        
        # Test get incidents
        url = '/appointments/api/staff/incidents/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test get recent incidents
        url = '/appointments/api/staff/incidents/recent/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_medication_endpoints(self):
        """Test medication management endpoints"""
        
        # Test create medication
        url = '/appointments/api/staff/medications/'
        medication_data = {
            'appointment': self.appointment.id,
            'name': 'Paracetamol',
            'strength': 500.0,
            'dose': 1000.0,
            'frequency': 'twice_daily',
            'administration_times': ['morning', 'evening'],
            'route': 'oral',
            'notes': 'Take with food'
        }
        response = self.api_client.post(url, medication_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = response.json()
        self.assertIn('id', data)
        self.assertIn('appointment', data)
        self.assertIn('name', data)
        self.assertIn('total_daily_dose', data)
        
        # Test get medications
        url = '/appointments/api/staff/medications/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test get medications by appointment
        url = f'/appointments/api/staff/medications/by_appointment/?appointment_id={self.appointment.id}'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_body_map_endpoints(self):
        """Test body map management endpoints"""
        
        # Test create body map
        url = '/appointments/api/staff/body-maps/'
        body_map_data = {
            'appointment': self.appointment.id,
            'body_regions': {
                'front': {'head': [], 'torso': [], 'arms': [], 'legs': []},
                'back': {'head': [], 'torso': [], 'arms': [], 'legs': []}
            },
            'injuries': [
                {
                    'location': 'left_arm',
                    'type': 'bruise',
                    'color': 'purple',
                    'size': '2cm',
                    'healing_stage': 'fresh',
                    'serious': False,
                    'notes': 'Minor bruise'
                }
            ],
            'consent_given': True,
            'consent_type': 'verbal',
            'consent_notes': 'Client gave verbal consent',
            'photography_consent': False,
            'photos_taken': False,
            'medical_referral': False,
            'police_notified': False,
            'safeguarding_referral': False,
            'notes': 'Routine body map examination',
            'follow_up_required': False
        }
        response = self.api_client.post(url, body_map_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = response.json()
        self.assertIn('id', data)
        self.assertIn('appointment', data)
        self.assertIn('injury_count', data)
        self.assertIn('has_serious_injuries', data)
        self.assertEqual(data['injury_count'], 1)
        self.assertEqual(data['has_serious_injuries'], False)
        
        # Test get body maps
        url = '/appointments/api/staff/body-maps/'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test get body maps by appointment
        url = f'/appointments/api/staff/body-maps/by_appointment/?appointment_id={self.appointment.id}'
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mobile_sync(self):
        """Test mobile sync endpoint"""
        
        url = '/appointments/api/staff/sync/'
        sync_data = {
            'appointments': [
                {
                    'id': self.appointment.id,
                    'checklist_items': ['medication', 'hygiene', 'breakfast', 'exercise']
                }
            ],
            'seizures': [
                {
                    'appointment': self.appointment.id,
                    'start_time': timezone.now().isoformat(),
                    'end_time': (timezone.now() + timedelta(minutes=5)).isoformat()
                }
            ]
        }
        response = self.api_client.post(url, sync_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('appointments_updated', data)
        self.assertIn('seizures_created', data)
        self.assertIn('incidents_created', data)
        self.assertIn('medications_created', data)
        self.assertIn('body_maps_created', data)
        self.assertIn('errors', data)

    def test_visit_validation(self):
        """Test visit validation scenarios"""
        
        # Test starting a visit that's already started
        self.appointment.actual_start_time = timezone.now()
        self.appointment.status = 'in_progress'
        self.appointment.save()
        
        url = f'/appointments/api/staff/appointments/{self.appointment.id}/start_visit/'
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test ending a visit that hasn't been started
        self.appointment.actual_start_time = None
        self.appointment.status = 'scheduled'
        self.appointment.save()
        
        url = f'/appointments/api/staff/appointments/{self.appointment.id}/end_visit/'
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test ending a visit that's already ended
        self.appointment.actual_start_time = timezone.now() - timedelta(hours=1)
        self.appointment.actual_end_time = timezone.now()
        self.appointment.status = 'completed'
        self.appointment.save()
        
        url = f'/appointments/api/staff/appointments/{self.appointment.id}/end_visit/'
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seizure_validation(self):
        """Test seizure validation scenarios"""
        
        # Create a seizure
        seizure = Seizure.objects.create(
            appointment=self.appointment,
            start_time=timezone.now()
        )
        
        # Test ending a seizure that's already ended
        seizure.end_time = timezone.now() + timedelta(minutes=5)
        seizure.save()
        
        url = f'/appointments/api/staff/seizures/{seizure.id}/end_seizure/'
        response = self.api_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incident_validation(self):
        """Test incident validation scenarios"""
        
        # Test creating incident with injury but no injury details
        url = '/appointments/api/staff/incidents/'
        incident_data = {
            'appointment': self.appointment.id,
            'time': timezone.now().isoformat(),
            'persons_involved': 'John Doe',
            'addresses_of_persons_involved': '123 Main St',
            'incident_details': 'Test incident',
            'was_person_injured': True,
            'person_injured': 'service_user',
            # Missing injury_details
            'incident_classification': ['other'],
            'remediation_taken': 'Documented',
            'incident_notifiable_riddor': False,
            'insurers_advised': False
        }
        response = self.api_client.post(url, incident_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_body_map_validation(self):
        """Test body map validation scenarios"""
        
        # Test creating body map with photos taken but no photography consent
        url = '/appointments/api/staff/body-maps/'
        body_map_data = {
            'appointment': self.appointment.id,
            'body_regions': {},
            'injuries': [],
            'consent_given': True,
            'consent_type': 'verbal',
            'photography_consent': False,
            'photos_taken': True,  # This should fail
            'medical_referral': False,
            'police_notified': False,
            'safeguarding_referral': False,
            'follow_up_required': False
        }
        response = self.api_client.post(url, body_map_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
