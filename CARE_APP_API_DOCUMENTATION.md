# Care App API Documentation

## Overview
The Care App API provides comprehensive endpoints for managing appointments, visits, and related care items for healthcare staff. This API is designed to support mobile applications and web interfaces for care management.

## Base URL
```
http://localhost:8000/
```

## Authentication

All API endpoints require authentication using Django REST Framework's token authentication or session authentication.

### Authentication Methods

You can authenticate using one of the following methods:

1. **Username & Password**
2. **6-digit Login Code (PIN)**
3. **Biometric ID**

### Login Endpoints

#### 1. Login (Multi-method)
**POST** `/api/auth/login/`

Request body (one of the following):
```json
// Username & Password
{
  "username": "nurse_jane",
  "password": "your_password"
}

// Login Code
{
  "login_code": "123456"
}

// Biometric ID
{
  "biometric_id": "biometric-uuid-string"
}
```

**Response:**
```json
{
  "token": "<auth_token>",
  "user_id": 1,
  "username": "nurse_jane",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "staff": {
    "id": 1,
    "username": "nurse_jane",
    "first_name": "Jane",
    "last_name": "Doe",
    "full_name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "1234567890",
    "role": "nurse",
    "role_display": "Nurse",
    "is_active": true,
    "is_staff_member": true,
    "has_login_code": true,
    "has_biometric": true
  }
}
```

#### 2. Login with Code
**POST** `/api/auth/login/code/`

Request body:
```json
{
  "login_code": "123456"
}
```

**Response:**
```json
{
  "token": "<auth_token>",
  "user_id": 1,
  "username": "nurse_jane",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "staff": { ... }
}
```

#### 3. Login with Biometric
**POST** `/api/auth/login/biometric/`

Request body:
```json
{
  "biometric_id": "biometric-uuid-string"
}
```

**Response:**
```json
{
  "token": "<auth_token>",
  "user_id": 1,
  "username": "nurse_jane",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane@example.com",
  "staff": { ... }
}
```

### Error Responses
- If the credentials or code are invalid, or the user is not a staff member, you will receive:
```json
{
  "error": "Invalid username or password, or user is not a staff member"
}
```
- For login code:
```json
{
  "error": "Invalid login code or user is not a staff member"
}
```

### Headers
```
Authorization: Token <your_token>
Content-Type: application/json
```

---

## API Endpoints

### 1. Staff Dashboard
**GET** `/appointments/api/staff/dashboard/`

Returns comprehensive dashboard data for the authenticated staff member.

**Response:**
```json
{
  "today_appointments": [
    {
      "id": 1,
      "title": "Morning Care Visit",
      "description": "Daily morning care routine",
      "start_time": "2024-01-15T09:00:00Z",
      "end_time": "2024-01-15T10:00:00Z",
      "status": "scheduled",
      "client": 1,
      "client_name": "John Smith",
      "frequency": "daily",
      "assigned_staff": 1,
      "assigned_staff_name": "nurse_jane",
      "actual_start_time": null,
      "actual_end_time": null,
      "checklist_items": [],
      "duration_minutes": null,
      "available_checklist_items": ["medication", "hygiene", "breakfast"],
      "checklist_completion_percentage": 0.0,
      "created_at": "2024-01-15T08:00:00Z",
      "updated_at": "2024-01-15T08:00:00Z"
    }
  ],
  "in_progress_appointments": [],
  "upcoming_appointments": [],
  "recent_incidents": [],
  "recent_seizures": [],
  "stats": {
    "today_count": 1,
    "in_progress_count": 0,
    "upcoming_count": 0,
    "recent_incidents_count": 0,
    "recent_seizures_count": 0
  }
}
```

### 2. Staff Appointments

#### Get All Appointments
**GET** `/appointments/api/staff/appointments/`

Returns all appointments assigned to the authenticated staff member.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Morning Care Visit",
    "description": "Daily morning care routine",
    "start_time": "2024-01-15T09:00:00Z",
    "end_time": "2024-01-15T10:00:00Z",
    "status": "scheduled",
    "client": 1,
    "client_name": "John Smith",
    "frequency": "daily",
    "assigned_staff": 1,
    "assigned_staff_name": "nurse_jane",
    "actual_start_time": null,
    "actual_end_time": null,
    "checklist_items": [],
    "duration_minutes": null,
    "available_checklist_items": ["medication", "hygiene", "breakfast"],
    "checklist_completion_percentage": 0.0,
    "created_at": "2024-01-15T08:00:00Z",
    "updated_at": "2024-01-15T08:00:00Z"
  }
]
```

#### Get Today's Appointments
**GET** `/appointments/api/staff/appointments/today/`

Returns appointments scheduled for today.

#### Get Upcoming Appointments
**GET** `/appointments/api/staff/appointments/upcoming/`

Returns the next 10 upcoming appointments.

#### Get In-Progress Appointments
**GET** `/appointments/api/staff/appointments/in_progress/`

Returns currently in-progress appointments.

#### Get This Week's Appointments
**GET** `/appointments/api/staff/appointments/week/`

Returns all appointments for the current week (Monday–Sunday) assigned to the authenticated staff member.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Morning Care Visit",
    "description": "Daily morning care routine",
    "start_time": "2024-01-15T09:00:00Z",
    "end_time": "2024-01-15T10:00:00Z",
    "status": "scheduled",
    "client": 1,
    "client_name": "John Smith",
    "frequency": "daily",
    "assigned_staff": 1,
    "assigned_staff_name": "nurse_jane",
    "actual_start_time": null,
    "actual_end_time": null,
    "checklist_items": [],
    "duration_minutes": null,
    "available_checklist_items": ["medication", "hygiene", "breakfast"],
    "checklist_completion_percentage": 0.0,
    "created_at": "2024-01-15T08:00:00Z",
    "updated_at": "2024-01-15T08:00:00Z"
  }
]
```

#### Start Visit
**POST** `/appointments/api/staff/appointments/{id}/start_visit/`

Starts a visit by setting the actual start time.

**Response:**
```json
{
  "message": "Visit started successfully",
  "actual_start_time": "2024-01-15T09:05:00Z"
}
```

#### End Visit
**POST** `/appointments/api/staff/appointments/{id}/end_visit/`

Ends a visit by setting the actual end time.

**Response:**
```json
{
  "message": "Visit ended successfully",
  "actual_end_time": "2024-01-15T10:15:00Z",
  "duration_minutes": 70
}
```

#### Update Checklist
**POST** `/appointments/api/staff/appointments/{id}/update_checklist/`

Updates checklist items for an appointment.

**Request:**
```json
{
  "checklist_items": ["medication", "hygiene", "breakfast"]
}
```

**Response:**
```json
{
  "message": "Checklist updated successfully",
  "checklist_items": ["medication", "hygiene", "breakfast"],
  "completion_percentage": 100.0
}
```

#### Create Appointment
**POST** `/appointments/api/staff/appointments/`

Creates a new appointment.

**Request:**
```json
{
  "title": "Evening Care Visit",
  "description": "Evening care routine",
  "client": 1,
  "start_time": "2024-01-15T18:00:00Z",
  "end_time": "2024-01-15T19:00:00Z",
  "status": "scheduled",
  "frequency": "daily",
  "assigned_staff": 1
}
```

#### Update Appointment
**PUT** `/appointments/api/staff/appointments/{id}/`

Updates an existing appointment.

#### Delete Appointment
**DELETE** `/appointments/api/staff/appointments/{id}/`

Deletes an appointment.

#### Get Appointment Details
**GET** `/appointments/api/staff/appointments/{id}/details/`

Returns all details for a single appointment, including:
- title, description, start time, end time, status
- full linked client details (nested)
- all notes for that appointment (with content, document, uploaded_by, timestamps, etc.)

**Response:**
```json
{
  "id": 1,
  "title": "Morning Care Visit",
  "description": "Daily morning care routine",
  "start_time": "2024-01-15T09:00:00Z",
  "end_time": "2024-01-15T10:00:00Z",
  "status": "scheduled",
  "client": {
    "id": 1,
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@example.com",
    "phone": "1234567890",
    "address": "123 Main St",
    "care_checklist": ["medication", "hygiene"],
    "invoice_group": null,
    "full_name": "John Smith",
    "full_address": "123 Main St",
    "created_at": "2024-01-01T08:00:00Z",
    "updated_at": "2024-01-10T08:00:00Z"
  },
  "frequency": "daily",
  "assigned_staff": 2,
  "actual_start_time": null,
  "actual_end_time": null,
  "checklist_items": [],
  "duration_minutes": null,
  "available_checklist_items": ["medication", "hygiene"],
  "checklist_completion_percentage": 0.0,
  "created_at": "2024-01-15T08:00:00Z",
  "updated_at": "2024-01-15T08:00:00Z",
  "notes": [
    {
      "id": 1,
      "content": "Checked blood pressure.",
      "document": null,
      "uploaded_by": 2,
      "uploaded_by_username": "nurse_jane",
      "created_at": "2024-01-15T09:10:00Z",
      "updated_at": "2024-01-15T09:10:00Z"
    },
    {
      "id": 2,
      "content": "Administered medication.",
      "document": null,
      "uploaded_by": 2,
      "uploaded_by_username": "nurse_jane",
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z"
    }
  ]
}
```

### 3. Seizures

#### Get All Seizures
**GET** `/appointments/api/staff/seizures/`

Returns all seizures for appointments assigned to the staff member.

**Response:**
```json
[
  {
    "id": 1,
    "appointment": 1,
    "appointment_title": "Morning Care Visit",
    "client_name": "John Smith",
    "start_time": "2024-01-15T09:30:00Z",
    "end_time": "2024-01-15T09:35:00Z",
    "duration_minutes": 5,
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:35:00Z"
  }
]
```

#### Create Seizure
**POST** `/appointments/api/staff/seizures/`

Creates a new seizure record.

**Request:**
```json
{
  "appointment": 1,
  "start_time": "2024-01-15T09:30:00Z"
}
```

#### End Seizure
**POST** `/appointments/api/staff/seizures/{id}/end_seizure/`

Ends a seizure by setting the end time.

**Response:**
```json
{
  "message": "Seizure ended successfully",
  "end_time": "2024-01-15T09:35:00Z",
  "duration_minutes": 5
}
```

#### Update Seizure
**PUT** `/appointments/api/staff/seizures/{id}/`

Updates an existing seizure.

#### Delete Seizure
**DELETE** `/appointments/api/staff/seizures/{id}/`

Deletes a seizure.

### 4. Incidents

#### Get All Incidents
**GET** `/appointments/api/staff/incidents/`

Returns all incidents for appointments assigned to the staff member.

**Response:**
```json
[
  {
    "id": 1,
    "appointment": 1,
    "appointment_title": "Morning Care Visit",
    "client_name": "John Smith",
    "time": "2024-01-15T09:45:00Z",
    "persons_involved": "John Doe, Jane Smith",
    "addresses_of_persons_involved": "123 Main St",
    "incident_details": "Client fell while walking",
    "was_person_injured": true,
    "person_injured": "service_user",
    "person_injured_display": "Service User",
    "injury_details": "Minor bruise on left arm",
    "incident_classification": ["minor_injury"],
    "remediation_taken": "Applied ice pack",
    "incident_notifiable_riddor": false,
    "f2508_document": null,
    "other_people_notified": "Supervisor informed",
    "additional_information": "Client was assisted back to bed",
    "insurers_advised": false,
    "created_at": "2024-01-15T09:45:00Z",
    "updated_at": "2024-01-15T09:45:00Z"
  }
]
```

#### Get Recent Incidents
**GET** `/appointments/api/staff/incidents/recent/`

Returns incidents from the last 30 days.

#### Create Incident
**POST** `/appointments/api/staff/incidents/`

Creates a new incident record.

**Request:**
```json
{
  "appointment": 1,
  "time": "2024-01-15T09:45:00Z",
  "persons_involved": "John Doe, Jane Smith",
  "addresses_of_persons_involved": "123 Main St",
  "incident_details": "Client fell while walking",
  "was_person_injured": true,
  "person_injured": "service_user",
  "injury_details": "Minor bruise on left arm",
  "incident_classification": ["minor_injury"],
  "remediation_taken": "Applied ice pack",
  "incident_notifiable_riddor": false,
  "other_people_notified": "Supervisor informed",
  "additional_information": "Client was assisted back to bed",
  "insurers_advised": false
}
```

#### Update Incident
**PUT** `/appointments/api/staff/incidents/{id}/`

Updates an existing incident.

#### Delete Incident
**DELETE** `/appointments/api/staff/incidents/{id}/`

Deletes an incident.

### 5. Medications

#### Get All Medications
**GET** `/appointments/api/staff/medications/`

Returns all medications for appointments assigned to the staff member.

**Response:**
```json
[
  {
    "id": 1,
    "appointment": 1,
    "appointment_title": "Morning Care Visit",
    "client_name": "John Smith",
    "name": "Paracetamol",
    "strength": 500.0,
    "dose": 1000.0,
    "frequency": "twice_daily",
    "frequency_display": "Twice Daily",
    "administration_times": ["morning", "evening"],
    "route": "oral",
    "route_display": "Oral",
    "notes": "Take with food",
    "total_daily_dose": 2000.0,
    "created_at": "2024-01-15T09:00:00Z",
    "updated_at": "2024-01-15T09:00:00Z"
  }
]
```

#### Get Medications by Appointment
**GET** `/appointments/api/staff/medications/by_appointment/?appointment_id=1`

Returns medications for a specific appointment.

#### Create Medication
**POST** `/appointments/api/staff/medications/`

Creates a new medication record.

**Request:**
```json
{
  "appointment": 1,
  "name": "Paracetamol",
  "strength": 500.0,
  "dose": 1000.0,
  "frequency": "twice_daily",
  "administration_times": ["morning", "evening"],
  "route": "oral",
  "notes": "Take with food"
}
```

#### Update Medication
**PUT** `/appointments/api/staff/medications/{id}/`

Updates an existing medication.

#### Delete Medication
**DELETE** `/appointments/api/staff/medications/{id}/`

Deletes a medication.

### 6. Body Maps

#### Get All Body Maps
**GET** `/appointments/api/staff/body-maps/`

Returns all body maps for appointments assigned to the staff member.

**Response:**
```json
[
  {
    "id": 1,
    "appointment": 1,
    "appointment_title": "Morning Care Visit",
    "client_name": "John Smith",
    "date_recorded": "2024-01-15T09:00:00Z",
    "practitioner": 1,
    "practitioner_name": "nurse_jane",
    "body_regions": {
      "front": {"head": [], "torso": [], "arms": [], "legs": []},
      "back": {"head": [], "torso": [], "arms": [], "legs": []}
    },
    "injuries": [
      {
        "location": "left_arm",
        "type": "bruise",
        "color": "purple",
        "size": "2cm",
        "healing_stage": "fresh",
        "serious": false,
        "notes": "Minor bruise"
      }
    ],
    "injury_count": 1,
    "has_serious_injuries": false,
    "consent_given": true,
    "consent_type": "verbal",
    "consent_type_display": "Verbal Consent",
    "consent_notes": "Client gave verbal consent",
    "photography_consent": false,
    "photos_taken": false,
    "photo_documentation": null,
    "medical_referral": false,
    "medical_referral_details": null,
    "police_notified": false,
    "police_notification_details": null,
    "safeguarding_referral": false,
    "safeguarding_referral_details": null,
    "notes": "Routine body map examination",
    "follow_up_required": false,
    "follow_up_details": null,
    "created_at": "2024-01-15T09:00:00Z",
    "updated_at": "2024-01-15T09:00:00Z"
  }
]
```

#### Get Body Maps by Appointment
**GET** `/appointments/api/staff/body-maps/by_appointment/?appointment_id=1`

Returns body maps for a specific appointment.

#### Create Body Map
**POST** `/appointments/api/staff/body-maps/`

Creates a new body map record.

**Request:**
```json
{
  "appointment": 1,
  "body_regions": {
    "front": {"head": [], "torso": [], "arms": [], "legs": []},
    "back": {"head": [], "torso": [], "arms": [], "legs": []}
  },
  "injuries": [
    {
      "location": "left_arm",
      "type": "bruise",
      "color": "purple",
      "size": "2cm",
      "healing_stage": "fresh",
      "serious": false,
      "notes": "Minor bruise"
    }
  ],
  "consent_given": true,
  "consent_type": "verbal",
  "consent_notes": "Client gave verbal consent",
  "photography_consent": false,
  "photos_taken": false,
  "medical_referral": false,
  "police_notified": false,
  "safeguarding_referral": false,
  "notes": "Routine body map examination",
  "follow_up_required": false
}
```

#### Update Body Map
**PUT** `/appointments/api/staff/body-maps/{id}/`

Updates an existing body map.

#### Delete Body Map
**DELETE** `/appointments/api/staff/body-maps/{id}/`

Deletes a body map.

### 7. Mobile Sync

#### Sync Data
**POST** `/appointments/api/staff/sync/`

Synchronizes data from the mobile app to the server.

**Request:**
```json
{
  "appointments": [
    {
      "id": 1,
      "checklist_items": ["medication", "hygiene", "breakfast", "exercise"]
    }
  ],
  "seizures": [
    {
      "appointment": 1,
      "start_time": "2024-01-15T09:30:00Z",
      "end_time": "2024-01-15T09:35:00Z"
    }
  ],
  "incidents": [
    {
      "appointment": 1,
      "time": "2024-01-15T09:45:00Z",
      "persons_involved": "John Doe",
      "addresses_of_persons_involved": "123 Main St",
      "incident_details": "Test incident",
      "was_person_injured": false,
      "incident_classification": ["other"],
      "remediation_taken": "Documented",
      "incident_notifiable_riddor": false,
      "insurers_advised": false
    }
  ],
  "medications": [
    {
      "appointment": 1,
      "name": "Paracetamol",
      "strength": 500.0,
      "dose": 1000.0,
      "frequency": "twice_daily",
      "administration_times": ["morning", "evening"],
      "route": "oral",
      "notes": "Take with food"
    }
  ],
  "body_maps": [
    {
      "appointment": 1,
      "body_regions": {},
      "injuries": [],
      "consent_given": true,
      "consent_type": "verbal",
      "photography_consent": false,
      "photos_taken": false,
      "medical_referral": false,
      "police_notified": false,
      "safeguarding_referral": false,
      "follow_up_required": false
    }
  ]
}
```

**Response:**
```json
{
  "appointments_updated": 1,
  "seizures_created": 1,
  "incidents_created": 1,
  "medications_created": 1,
  "body_maps_created": 1,
  "errors": []
}
```

## Data Models

### Appointment
```json
{
  "id": 1,
  "title": "Morning Care Visit",
  "description": "Daily morning care routine",
  "start_time": "2024-01-15T09:00:00Z",
  "end_time": "2024-01-15T10:00:00Z",
  "status": "scheduled",
  "client": 1,
  "client_name": "John Smith",
  "frequency": "daily",
  "assigned_staff": 1,
  "assigned_staff_name": "nurse_jane",
  "actual_start_time": "2024-01-15T09:05:00Z",
  "actual_end_time": "2024-01-15T10:15:00Z",
  "checklist_items": ["medication", "hygiene", "breakfast"],
  "duration_minutes": 70,
  "available_checklist_items": ["medication", "hygiene", "breakfast", "exercise"],
  "checklist_completion_percentage": 75.0,
  "created_at": "2024-01-15T08:00:00Z",
  "updated_at": "2024-01-15T10:15:00Z"
}
```

**Status Options:**
- `scheduled` - Appointment is scheduled but not started
- `in_progress` - Visit is currently in progress
- `completed` - Visit has been completed
- `cancelled` - Appointment has been cancelled
- `no_show` - Client did not show up

### Seizure
```json
{
  "id": 1,
  "appointment": 1,
  "appointment_title": "Morning Care Visit",
  "client_name": "John Smith",
  "start_time": "2024-01-15T09:30:00Z",
  "end_time": "2024-01-15T09:35:00Z",
  "duration_minutes": 5,
  "created_at": "2024-01-15T09:30:00Z",
  "updated_at": "2024-01-15T09:35:00Z"
}
```

### Incident
```json
{
  "id": 1,
  "appointment": 1,
  "appointment_title": "Morning Care Visit",
  "client_name": "John Smith",
  "time": "2024-01-15T09:45:00Z",
  "persons_involved": "John Doe, Jane Smith",
  "addresses_of_persons_involved": "123 Main St",
  "incident_details": "Client fell while walking",
  "was_person_injured": true,
  "person_injured": "service_user",
  "person_injured_display": "Service User",
  "injury_details": "Minor bruise on left arm",
  "incident_classification": ["minor_injury"],
  "remediation_taken": "Applied ice pack",
  "incident_notifiable_riddor": false,
  "f2508_document": null,
  "other_people_notified": "Supervisor informed",
  "additional_information": "Client was assisted back to bed",
  "insurers_advised": false,
  "created_at": "2024-01-15T09:45:00Z",
  "updated_at": "2024-01-15T09:45:00Z"
}
```

**Person Injured Options:**
- `service_user` - Service User
- `carer` - Carer
- `visitor` - Visitor
- `other` - Other

**Incident Classification Options:**
- `minor_injury` - Minor Injury
- `major_injury` - Major Injury
- `injury_3_days_sick_leave` - Injury Required More Than 3 Days Sick Leave
- `admitted_hospital` - Admitted or Taken to Hospital
- `fatality` - Fatality
- `self_harm_overdose` - Self Harm (Overdose)
- `self_harm_other` - Self Harm (Other)
- `verbal_abuse` - Verbal Abuse
- `physical_abuse` - Physical Abuse
- `assault` - Assault
- `arson` - Arson
- `damage_theft_property` - Damage to/Theft of Property
- `substance_misuse` - Substance Misuse
- `other` - Other

### Medication
```json
{
  "id": 1,
  "appointment": 1,
  "appointment_title": "Morning Care Visit",
  "client_name": "John Smith",
  "name": "Paracetamol",
  "strength": 500.0,
  "dose": 1000.0,
  "frequency": "twice_daily",
  "frequency_display": "Twice Daily",
  "administration_times": ["morning", "evening"],
  "route": "oral",
  "route_display": "Oral",
  "notes": "Take with food",
  "total_daily_dose": 2000.0,
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T09:00:00Z"
}
```

**Frequency Options:**
- `once_daily` - Once Daily
- `twice_daily` - Twice Daily
- `three_times_daily` - Three Times Daily
- `four_times_daily` - Four Times Daily
- `every_4_hours` - Every 4 Hours
- `every_6_hours` - Every 6 Hours
- `every_8_hours` - Every 8 Hours
- `every_12_hours` - Every 12 Hours
- `as_needed` - As Needed (PRN)
- `before_meals` - Before Meals
- `after_meals` - After Meals
- `with_meals` - With Meals
- `at_bedtime` - At Bedtime
- `weekly` - Weekly
- `monthly` - Monthly
- `other` - Other

**Administration Time Options:**
- `morning` - Morning (8:00 AM)
- `mid_morning` - Mid-Morning (10:00 AM)
- `noon` - Noon (12:00 PM)
- `afternoon` - Afternoon (2:00 PM)
- `evening` - Evening (6:00 PM)
- `night` - Night (8:00 PM)
- `bedtime` - Bedtime (10:00 PM)
- `before_breakfast` - Before Breakfast
- `after_breakfast` - After Breakfast
- `before_lunch` - Before Lunch
- `after_lunch` - After Lunch
- `before_dinner` - Before Dinner
- `after_dinner` - After Dinner
- `as_needed` - As Needed
- `other` - Other

**Route Options:**
- `oral` - Oral
- `buccal` - Buccal
- `sublingual` - Sublingual
- `intravenous` - Intravenous (IV)
- `intramuscular` - Intramuscular (IM)
- `subcutaneous` - Subcutaneous (SC)
- `topical` - Topical
- `inhalation` - Inhalation
- `nasal` - Nasal
- `ophthalmic` - Ophthalmic (Eye)
- `otic` - Otic (Ear)
- `rectal` - Rectal
- `transdermal` - Transdermal
- `other` - Other

### Body Map
```json
{
  "id": 1,
  "appointment": 1,
  "appointment_title": "Morning Care Visit",
  "client_name": "John Smith",
  "date_recorded": "2024-01-15T09:00:00Z",
  "practitioner": 1,
  "practitioner_name": "nurse_jane",
  "body_regions": {
    "front": {"head": [], "torso": [], "arms": [], "legs": []},
    "back": {"head": [], "torso": [], "arms": [], "legs": []}
  },
  "injuries": [
    {
      "location": "left_arm",
      "type": "bruise",
      "color": "purple",
      "size": "2cm",
      "healing_stage": "fresh",
      "serious": false,
      "notes": "Minor bruise"
    }
  ],
  "injury_count": 1,
  "has_serious_injuries": false,
  "consent_given": true,
  "consent_type": "verbal",
  "consent_type_display": "Verbal Consent",
  "consent_notes": "Client gave verbal consent",
  "photography_consent": false,
  "photos_taken": false,
  "photo_documentation": null,
  "medical_referral": false,
  "medical_referral_details": null,
  "police_notified": false,
  "police_notification_details": null,
  "safeguarding_referral": false,
  "safeguarding_referral_details": null,
  "notes": "Routine body map examination",
  "follow_up_required": false,
  "follow_up_details": null,
  "created_at": "2024-01-15T09:00:00Z",
  "updated_at": "2024-01-15T09:00:00Z"
}
```

**Injury Type Options:**
- `pressure_ulcer` - Pressure Ulcer
- `cut` - Cut/Laceration
- `abrasion` - Abrasion/Scrape
- `burn` - Burn
- `swelling` - Swelling
- `redness` - Redness
- `scar` - Scar
- `tenderness` - Tenderness
- `bruise` - Bruise
- `other` - Other

**Injury Color Options:**
- `red` - Red
- `purple` - Purple
- `blue` - Blue
- `green` - Green
- `yellow` - Yellow
- `brown` - Brown
- `black` - Black
- `pink` - Pink
- `white` - White
- `other` - Other

**Healing Stage Options:**
- `fresh` - Fresh (0-24 hours)
- `early` - Early Healing (1-3 days)
- `intermediate` - Intermediate (3-7 days)
- `late` - Late Healing (1-2 weeks)
- `healed` - Healed
- `unknown` - Unknown

**Consent Type Options:**
- `verbal` - Verbal Consent
- `written` - Written Consent
- `implied` - Implied Consent
- `emergency` - Emergency Treatment
- `guardian` - Guardian Consent
- `none` - No Consent Given

## Error Responses

### Validation Error
```json
{
  "error": "Validation error message"
}
```

### Not Found
```json
{
  "error": "Resource not found"
}
```

### Permission Denied
```json
{
  "error": "You do not have permission to perform this action"
}
```

### Bad Request
```json
{
  "error": "Bad request message"
}
```

## Usage Examples

### Starting a Visit
```javascript
// Start a visit
fetch('/appointments/api/staff/appointments/1/start_visit/', {
  method: 'POST',
  headers: {
    'Authorization': 'Token your_token_here',
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

### Creating a Seizure Record
```javascript
// Create a seizure
fetch('/appointments/api/staff/seizures/', {
  method: 'POST',
  headers: {
    'Authorization': 'Token your_token_here',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    appointment: 1,
    start_time: new Date().toISOString()
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Getting Today's Appointments
```javascript
// Get today's appointments
fetch('/appointments/api/staff/appointments/today/', {
  headers: {
    'Authorization': 'Token your_token_here'
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

### Updating Checklist
```javascript
// Update checklist
fetch('/appointments/api/staff/appointments/1/update_checklist/', {
  method: 'POST',
  headers: {
    'Authorization': 'Token your_token_here',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    checklist_items: ['medication', 'hygiene', 'breakfast', 'exercise']
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Creating an Incident
```javascript
// Create an incident
fetch('/appointments/api/staff/incidents/', {
  method: 'POST',
  headers: {
    'Authorization': 'Token your_token_here',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    appointment: 1,
    time: new Date().toISOString(),
    persons_involved: 'John Doe',
    addresses_of_persons_involved: '123 Main St',
    incident_details: 'Client fell while walking',
    was_person_injured: true,
    person_injured: 'service_user',
    injury_details: 'Minor bruise on left arm',
    incident_classification: ['minor_injury'],
    remediation_taken: 'Applied ice pack',
    incident_notifiable_riddor: false,
    insurers_advised: false
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Notes

1. **Authentication**: All endpoints require authentication. Use token authentication for mobile apps and session authentication for web interfaces.

2. **Staff Access**: Staff members can only access data for appointments assigned to them.

3. **Timestamps**: All timestamps are in ISO 8601 format (UTC).

4. **Validation**: The API enforces validation rules:
   - Injury details are required if someone was injured in an incident
   - F2508 document is required if incident is RIDDOR notifiable
   - Consent type is required if consent was given for body map
   - Photography consent is required if photos were taken

5. **Mobile Sync**: The sync endpoint allows for offline data synchronization.

6. **Calculated Fields**: Some fields are calculated automatically:
   - `duration_minutes` for appointments and seizures
   - `total_daily_dose` for medications
   - `injury_count` and `has_serious_injuries` for body maps
   - `checklist_completion_percentage` for appointments

7. **File Uploads**: For incidents requiring F2508 documents, use multipart/form-data encoding.

8. **Pagination**: List endpoints may implement pagination for large datasets.

9. **Filtering**: Some endpoints support query parameters for filtering:
   - `by_appointment` for medications and body maps
   - `recent` for incidents

10. **Error Handling**: Always check HTTP status codes and handle errors appropriately in your application. 