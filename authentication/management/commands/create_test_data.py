from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from client_management.models import Client
from appointment_management.models import Appointment

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test data for mobile app testing'

    def handle(self, *args, **options):
        # Get the test user
        try:
            user = User.objects.get(username='nurse_test')
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Test user not found. Run create_test_user first.')
            )
            return

        # Create test client if it doesn't exist
        client, created = Client.objects.get_or_create(
            email='john.smith@example.com',
            defaults={
                'first_name': 'John',
                'last_name': 'Smith',
                'phone': '+1234567890',
                'address': '123 Main Street, Anytown, USA',
                'care_checklist': ['medication', 'hygiene', 'breakfast', 'exercise']
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created test client: {client.full_name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Test client already exists: {client.full_name}')
            )

        # Create test appointments
        today = timezone.now().date()
        now = timezone.now()
        
        # Today's appointments
        appointments_data = [
            {
                'title': 'Morning Care Visit',
                'description': 'Daily morning care routine including medication and hygiene',
                'start_time': timezone.now().replace(hour=9, minute=0, second=0, microsecond=0),
                'end_time': timezone.now().replace(hour=10, minute=0, second=0, microsecond=0),
                'status': 'scheduled',
                'frequency': 'daily'
            },
            {
                'title': 'Afternoon Medication',
                'description': 'Administer afternoon medications',
                'start_time': timezone.now().replace(hour=14, minute=0, second=0, microsecond=0),
                'end_time': timezone.now().replace(hour=14, minute=30, second=0, microsecond=0),
                'status': 'scheduled',
                'frequency': 'daily'
            },
            {
                'title': 'Evening Care Visit',
                'description': 'Evening care routine and medication',
                'start_time': timezone.now().replace(hour=18, minute=0, second=0, microsecond=0),
                'end_time': timezone.now().replace(hour=19, minute=0, second=0, microsecond=0),
                'status': 'scheduled',
                'frequency': 'daily'
            }
        ]

        created_count = 0
        for appt_data in appointments_data:
            appointment, created = Appointment.objects.get_or_create(
                title=appt_data['title'],
                client=client,
                start_time=appt_data['start_time'],
                defaults={
                    'description': appt_data['description'],
                    'end_time': appt_data['end_time'],
                    'status': appt_data['status'],
                    'frequency': appt_data['frequency'],
                    'assigned_staff': user,
                    'checklist_items': []
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created appointment: {appointment.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Appointment already exists: {appointment.title}')
                )

        # Create some upcoming appointments
        tomorrow = today + timedelta(days=1)
        upcoming_appointments_data = [
            {
                'title': 'Morning Care Visit',
                'description': 'Daily morning care routine',
                'start_time': (timezone.now() + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0),
                'end_time': (timezone.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0),
                'status': 'scheduled',
                'frequency': 'daily'
            },
            {
                'title': 'Weekly Assessment',
                'description': 'Weekly health and care assessment',
                'start_time': (timezone.now() + timedelta(days=3)).replace(hour=10, minute=0, second=0, microsecond=0),
                'end_time': (timezone.now() + timedelta(days=3)).replace(hour=11, minute=0, second=0, microsecond=0),
                'status': 'scheduled',
                'frequency': 'weekly'
            }
        ]

        for appt_data in upcoming_appointments_data:
            appointment, created = Appointment.objects.get_or_create(
                title=appt_data['title'],
                client=client,
                start_time=appt_data['start_time'],
                defaults={
                    'description': appt_data['description'],
                    'end_time': appt_data['end_time'],
                    'status': appt_data['status'],
                    'frequency': appt_data['frequency'],
                    'assigned_staff': user,
                    'checklist_items': []
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created upcoming appointment: {appointment.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTest Data Summary:')
        )
        self.stdout.write(f'Client: {client.full_name}')
        self.stdout.write(f'User: {user.full_name} ({user.get_role_display()})')
        self.stdout.write(f'Total appointments created: {created_count}')
        self.stdout.write(f'Today\'s appointments: {Appointment.objects.filter(assigned_staff=user, start_time__date=today).count()}')
        self.stdout.write(f'Upcoming appointments: {Appointment.objects.filter(assigned_staff=user, start_time__date__gt=today).count()}')
        
        self.stdout.write(f'\nTest the dashboard API:')
        self.stdout.write(f'GET http://localhost:8000/appointments/api/staff/dashboard/')
        self.stdout.write(f'Authorization: Token 8c5e41fabf0928db84178967f1d1aed240105f43') 