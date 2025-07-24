from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import requests
import json

from client_management.models import Client
from appointment_management.models import Appointment, Seizure, Incident, Medication, BodyMap

User = get_user_model()


class Command(BaseCommand):
    help = 'Test all visit management API endpoints'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting visit management API tests...'))
        
        # Create test data
        self.create_test_data()
        
        # Test all endpoints
        self.test_staff_dashboard()
        self.test_appointment_endpoints()
        self.test_seizure_endpoints()
        self.test_incident_endpoints()
        self.test_medication_endpoints()
        self.test_body_map_endpoints()
        self.test_mobile_sync()
        
        self.stdout.write(self.style.SUCCESS('All tests completed!'))

    def create_test_data(self):
        """Create test data for API testing"""
        self.stdout.write('Creating test data...')
        
        # Clean up any existing test data
        try:
            # Delete related data first
            Appointment.objects.filter(title='Test Visit').delete()
            User.objects.filter(username='test_staff').delete()
            Client.objects.filter(email='john@example.com').delete()
        except:
            pass
        
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
            assigned_staff=self.user
        )
        
        # Create API client
        self.api_client = requests.Session()
        self.api_client.auth = (self.user.username, 'testpass123')

    def test_staff_dashboard(self):
        """Test staff dashboard endpoint"""
        self.stdout.write('Testing staff dashboard...')
        
        url = 'http://localhost:8000/appointments/api/staff/dashboard/'
        response = self.api_client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            self.stdout.write(f'✓ Dashboard loaded successfully')
            self.stdout.write(f'  - Today appointments: {data["stats"]["today_count"]}')
            self.stdout.write(f'  - In progress: {data["stats"]["in_progress_count"]}')
            self.stdout.write(f'  - Upcoming: {data["stats"]["upcoming_count"]}')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Dashboard failed: {response.status_code}'))

    def test_appointment_endpoints(self):
        """Test appointment management endpoints"""
        self.stdout.write('Testing appointment endpoints...')
        
        # Test get all appointments
        url = 'http://localhost:8000/appointments/api/staff/appointments/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get appointments successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get appointments failed: {response.status_code}'))
        
        # Test get today's appointments
        url = 'http://localhost:8000/appointments/api/staff/appointments/today/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get today appointments successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get today appointments failed: {response.status_code}'))
        
        # Test get upcoming appointments
        url = 'http://localhost:8000/appointments/api/staff/appointments/upcoming/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get upcoming appointments successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get upcoming appointments failed: {response.status_code}'))
        
        # Test get in-progress appointments
        url = 'http://localhost:8000/appointments/api/staff/appointments/in_progress/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get in-progress appointments successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get in-progress appointments failed: {response.status_code}'))
        
        # Test start visit
        url = f'http://localhost:8000/appointments/api/staff/appointments/{self.appointment.id}/start_visit/'
        response = self.api_client.post(url)
        if response.status_code == 200:
            self.stdout.write('✓ Start visit successful')
            data = response.json()
            self.stdout.write(f'  - Actual start time: {data["actual_start_time"]}')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Start visit failed: {response.status_code}'))
        
        # Test update checklist
        url = f'http://localhost:8000/appointments/api/staff/appointments/{self.appointment.id}/update_checklist/'
        data = {'checklist_items': ['medication', 'hygiene', 'breakfast']}
        response = self.api_client.post(url, json=data)
        if response.status_code == 200:
            self.stdout.write('✓ Update checklist successful')
            data = response.json()
            self.stdout.write(f'  - Completion percentage: {data["completion_percentage"]}%')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Update checklist failed: {response.status_code}'))
        
        # Test end visit
        url = f'http://localhost:8000/appointments/api/staff/appointments/{self.appointment.id}/end_visit/'
        response = self.api_client.post(url)
        if response.status_code == 200:
            self.stdout.write('✓ End visit successful')
            data = response.json()
            self.stdout.write(f'  - Duration: {data["duration_minutes"]} minutes')
        else:
            self.stdout.write(self.style.ERROR(f'✗ End visit failed: {response.status_code}'))

    def test_seizure_endpoints(self):
        """Test seizure management endpoints"""
        self.stdout.write('Testing seizure endpoints...')
        
        # Test create seizure
        url = 'http://localhost:8000/appointments/api/staff/seizures/'
        data = {
            'appointment': self.appointment.id,
            'start_time': timezone.now().isoformat()
        }
        response = self.api_client.post(url, json=data)
        if response.status_code == 201:
            self.stdout.write('✓ Create seizure successful')
            seizure_id = response.json()['id']
            
            # Test end seizure
            url = f'http://localhost:8000/appointments/api/staff/seizures/{seizure_id}/end_seizure/'
            response = self.api_client.post(url)
            if response.status_code == 200:
                self.stdout.write('✓ End seizure successful')
                data = response.json()
                self.stdout.write(f'  - Duration: {data["duration_seconds"]} seconds')
            else:
                self.stdout.write(self.style.ERROR(f'✗ End seizure failed: {response.status_code}'))
        else:
            self.stdout.write(self.style.ERROR(f'✗ Create seizure failed: {response.status_code}'))
        
        # Test get seizures
        url = 'http://localhost:8000/appointments/api/staff/seizures/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get seizures successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get seizures failed: {response.status_code}'))

    def test_incident_endpoints(self):
        """Test incident management endpoints"""
        self.stdout.write('Testing incident endpoints...')
        
        # Test create incident
        url = 'http://localhost:8000/appointments/api/staff/incidents/'
        data = {
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
        response = self.api_client.post(url, json=data)
        if response.status_code == 201:
            self.stdout.write('✓ Create incident successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Create incident failed: {response.status_code}'))
        
        # Test get incidents
        url = 'http://localhost:8000/appointments/api/staff/incidents/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get incidents successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get incidents failed: {response.status_code}'))
        
        # Test get recent incidents
        url = 'http://localhost:8000/appointments/api/staff/incidents/recent/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get recent incidents successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get recent incidents failed: {response.status_code}'))

    def test_medication_endpoints(self):
        """Test medication management endpoints"""
        self.stdout.write('Testing medication endpoints...')
        
        # Test create medication
        url = 'http://localhost:8000/appointments/api/staff/medications/'
        data = {
            'appointment': self.appointment.id,
            'name': 'Paracetamol',
            'strength': 500.0,
            'dose': 1000.0,
            'frequency': 'twice_daily',
            'administration_times': ['morning', 'evening'],
            'route': 'oral',
            'notes': 'Take with food'
        }
        response = self.api_client.post(url, json=data)
        if response.status_code == 201:
            self.stdout.write('✓ Create medication successful')
            data = response.json()
            self.stdout.write(f'  - Total daily dose: {data["total_daily_dose"]}mg')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Create medication failed: {response.status_code}'))
        
        # Test get medications
        url = 'http://localhost:8000/appointments/api/staff/medications/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get medications successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get medications failed: {response.status_code}'))
        
        # Test get medications by appointment
        url = f'http://localhost:8000/appointments/api/staff/medications/by_appointment/?appointment_id={self.appointment.id}'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get medications by appointment successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get medications by appointment failed: {response.status_code}'))

    def test_body_map_endpoints(self):
        """Test body map management endpoints"""
        self.stdout.write('Testing body map endpoints...')
        
        # Test create body map
        url = 'http://localhost:8000/appointments/api/staff/body-maps/'
        data = {
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
        response = self.api_client.post(url, json=data)
        if response.status_code == 201:
            self.stdout.write('✓ Create body map successful')
            data = response.json()
            self.stdout.write(f'  - Injury count: {data["injury_count"]}')
            self.stdout.write(f'  - Has serious injuries: {data["has_serious_injuries"]}')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Create body map failed: {response.status_code}'))
        
        # Test get body maps
        url = 'http://localhost:8000/appointments/api/staff/body-maps/'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get body maps successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get body maps failed: {response.status_code}'))
        
        # Test get body maps by appointment
        url = f'http://localhost:8000/appointments/api/staff/body-maps/by_appointment/?appointment_id={self.appointment.id}'
        response = self.api_client.get(url)
        if response.status_code == 200:
            self.stdout.write('✓ Get body maps by appointment successful')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Get body maps by appointment failed: {response.status_code}'))

    def test_mobile_sync(self):
        """Test mobile sync endpoint"""
        self.stdout.write('Testing mobile sync endpoint...')
        
        url = 'http://localhost:8000/appointments/api/staff/sync/'
        data = {
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
        response = self.api_client.post(url, json=data)
        if response.status_code == 200:
            self.stdout.write('✓ Mobile sync successful')
            data = response.json()
            self.stdout.write(f'  - Appointments updated: {data["appointments_updated"]}')
            self.stdout.write(f'  - Seizures created: {data["seizures_created"]}')
        else:
            self.stdout.write(self.style.ERROR(f'✗ Mobile sync failed: {response.status_code}'))

    def cleanup(self):
        """Clean up test data"""
        self.stdout.write('Cleaning up test data...')
        try:
            self.user.delete()
            self.client_obj.delete()
        except:
            pass 