# Care App Mobile API Documentation

## Overview
This API provides endpoints for staff members to manage appointments, visits, and related care items through a mobile application.

## Authentication
All API endpoints require authentication using Django REST Framework's token authentication or session authentication.

### Headers
```
Authorization: Token <your_token>
Content-Type: application/json
```

## Base URL
```
https://your-domain.com/appointments/
```

## Endpoints

### 1. Staff Dashboard
**GET** `/api/staff/dashboard/`

Returns comprehensive dashboard data for the authenticated staff member.

**Response:**
```json
{
  "today_appointments": [...],
  "in_progress_appointments": [...],
  "upcoming_appointments": [...],
  "recent_incidents": [...],
  "recent_seizures": [...],
  "stats": {
    "today_count": 5,
    "in_progress_count": 2,
    "upcoming_count": 8,
    "recent_incidents_count": 1,
    "recent_seizures_count": 3
  }
}
```

### 2. Staff Appointments

#### Get All Appointments
**GET** `/api/staff/appointments/`

Returns all appointments assigned to the authenticated staff member.

#### Get Today's Appointments
**GET** `/api/staff/appointments/today/`

Returns appointments scheduled for today.

#### Get Upcoming Appointments
**GET** `/api/staff/appointments/upcoming/`

Returns the next 10 upcoming appointments.

#### Get In-Progress Appointments
**GET** `/api/staff/appointments/in_progress/`

Returns currently in-progress appointments.

#### Start Visit
**POST** `/api/staff/appointments/{id}/start_visit/`

Starts a visit by setting the actual start time.

**Response:**
```json
{
  "message": "Visit started successfully",
  "actual_start_time": "2024-01-15T10:30:00Z"
}
```

#### End Visit
**POST** `/api/staff/appointments/{id}/end_visit/`

Ends a visit by setting the actual end time.

**Response:**
```json
{
  "message": "Visit ended successfully",
  "actual_end_time": "2024-01-15T11:45:00Z",
  "duration_minutes": 75
}
```

#### Update Checklist
**POST** `/api/staff/appointments/{id}/update_checklist/`

Updates checklist items for an appointment.

**Request:**
```json
{
  "checklist_items": ["item1", "item2", "item3"]
}
```

**Response:**
```json
{
  "message": "Checklist updated successfully",
  "checklist_items": ["item1", "item2", "item3"],
  "completion_percentage": 60.0
}
```

### 3. Seizures

#### Get All Seizures
**GET** `/api/staff/seizures/`

Returns all seizures for appointments assigned to the staff member.

#### Create Seizure
**POST** `/api/staff/seizures/`

**Request:**
```json
{
  "appointment": 123,
  "start_time": "2024-01-15T10:30:00Z"
}
```

#### End Seizure
**POST** `/api/staff/seizures/{id}/end_seizure/`

Ends a seizure by setting the end time.

**Response:**
```json
{
  "message": "Seizure ended successfully",
  "end_time": "2024-01-15T10:35:00Z",
  "duration_minutes": 5
}
```

### 4. Incidents

#### Get All Incidents
**GET** `/api/staff/incidents/`

Returns all incidents for appointments assigned to the staff member.

#### Get Recent Incidents
**GET** `/api/staff/incidents/recent/`

Returns incidents from the last 30 days.

#### Create Incident
**POST** `/api/staff/incidents/`

**Request:**
```json
{
  "appointment": 123,
  "time": "2024-01-15T10:30:00Z",
  "persons_involved": "John Doe, Jane Smith",
  "addresses_of_persons_involved": "123 Main St, 456 Oak Ave",
  "incident_details": "Detailed description of the incident",
  "was_person_injured": true,
  "person_injured": "service_user",
  "injury_details": "Minor bruise on left arm",
  "incident_classification": ["minor_injury"],
  "remediation_taken": "Applied ice pack, documented incident",
  "incident_notifiable_riddor": false,
  "other_people_notified": "Supervisor informed",
  "additional_information": "Additional notes",
  "insurers_advised": false
}
```

### 5. Medications

#### Get All Medications
**GET** `/api/staff/medications/`

Returns all medications for appointments assigned to the staff member.

#### Get Medications by Appointment
**GET** `/api/staff/medications/by_appointment/?appointment_id=123`

Returns medications for a specific appointment.

#### Create Medication
**POST** `/api/staff/medications/`

**Request:**
```json
{
  "appointment": 123,
  "name": "Paracetamol",
  "strength": 500.0,
  "dose": 1000.0,
  "frequency": "twice_daily",
  "administration_times": ["morning", "evening"],
  "route": "oral",
  "notes": "Take with food"
}
```

### 6. Body Maps

#### Get All Body Maps
**GET** `/api/staff/body-maps/`

Returns all body maps for appointments assigned to the staff member.

#### Get Body Maps by Appointment
**GET** `/api/staff/body-maps/by_appointment/?appointment_id=123`

Returns body maps for a specific appointment.

#### Create Body Map
**POST** `/api/staff/body-maps/`

**Request:**
```json
{
  "appointment": 123,
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

### 7. Mobile Sync

#### Sync Data
**POST** `/api/staff/sync/`

Synchronizes data from the mobile app to the server.

**Request:**
```json
{
  "appointments": [
    {
      "id": 123,
      "checklist_items": ["item1", "item2"],
      "actual_start_time": "2024-01-15T10:30:00Z"
    }
  ],
  "seizures": [
    {
      "appointment": 123,
      "start_time": "2024-01-15T10:30:00Z",
      "end_time": "2024-01-15T10:35:00Z"
    }
  ],
  "incidents": [...],
  "medications": [...],
  "body_maps": [...]
}
```

**Response:**
```json
{
  "appointments_updated": 1,
  "seizures_created": 1,
  "incidents_created": 0,
  "medications_created": 0,
  "body_maps_created": 0,
  "errors": []
}
```

## Data Models

### Appointment
```json
{
  "id": 123,
  "title": "Morning Care Visit",
  "description": "Daily morning care routine",
  "start_time": "2024-01-15T09:00:00Z",
  "end_time": "2024-01-15T10:00:00Z",
  "status": "in_progress",
  "client": 456,
  "client_name": "John Smith",
  "frequency": "daily",
  "assigned_staff": 789,
  "assigned_staff_name": "nurse_jane",
  "actual_start_time": "2024-01-15T09:05:00Z",
  "actual_end_time": null,
  "checklist_items": ["medication", "hygiene", "breakfast"],
  "duration_minutes": null,
  "available_checklist_items": ["medication", "hygiene", "breakfast", "exercise"],
  "checklist_completion_percentage": 75.0,
  "created_at": "2024-01-15T08:00:00Z",
  "updated_at": "2024-01-15T09:05:00Z"
}
```

### Seizure
```json
{
  "id": 456,
  "appointment": 123,
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
  "id": 789,
  "appointment": 123,
  "appointment_title": "Morning Care Visit",
  "client_name": "John Smith",
  "time": "2024-01-15T09:45:00Z",
  "persons_involved": "John Smith, Jane Doe",
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

### Medication
```json
{
  "id": 101,
  "appointment": 123,
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

### Body Map
```json
{
  "id": 202,
  "appointment": 123,
  "appointment_title": "Morning Care Visit",
  "client_name": "John Smith",
  "date_recorded": "2024-01-15T09:00:00Z",
  "practitioner": 789,
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

## Usage Examples

### Starting a Visit
```javascript
// Start a visit
fetch('/appointments/api/staff/appointments/123/start_visit/', {
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
    appointment: 123,
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

## Notes

1. All timestamps are in ISO 8601 format (UTC)
2. Staff members can only access data for appointments assigned to them
3. The API automatically sets the practitioner for body maps to the authenticated staff member
4. Conditional validation is enforced for incidents (injury details required if injury occurred)
5. The mobile sync endpoint allows for offline data synchronization
6. All endpoints return appropriate HTTP status codes and error messages 