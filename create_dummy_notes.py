import os
import random

# Setup Django if running as a standalone script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'care_backend.settings')
import django
django.setup()

from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model
from appointment_management.models import Appointment
from visit_notes.models import Note

User = get_user_model()

# Get all appointments
appointments = Appointment.objects.all()
# Get all users
users = list(User.objects.filter(is_active=True))
# Get all images in static/images
image_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

if not image_files:
    print('No images found in static/images. Please add images first.')
    exit(1)

if not users:
    print('No active users found. Please create at least one user.')
    exit(1)

for appointment in appointments:
    for i in range(2):  # Create 2 notes per appointment
        img_path = random.choice(image_files)
        user = random.choice(users)
        note = Note(
            appointment=appointment,
            content=f"Dummy note {i+1} for appointment {appointment.id}",
            uploaded_by=user
        )
        with open(img_path, 'rb') as img_file:
            note.document.save(os.path.basename(img_path), File(img_file), save=True)
        note.save()
        print(f"Created note for appointment {appointment.id} with image {img_path}") 