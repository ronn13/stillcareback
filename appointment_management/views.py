from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.contrib.auth import get_user_model
import math
from .models import Appointment, Seizure, Incident, Medication, BodyMap, VisitLocationLog
from .forms import AppointmentForm, SeizureForm, IncidentForm, MedicationForm, BodyMapForm
from .serializers import (
    AppointmentSerializer, SeizureSerializer, IncidentSerializer, 
    MedicationSerializer, BodyMapSerializer, VisitLocationLogSerializer
)

User = get_user_model()


# Traditional Django Views
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/list.html'
    context_object_name = 'appointments'
    ordering = ['start_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.is_staff_member:
            # Filter by assigned staff if user is staff member
            queryset = queryset.filter(assigned_staff=self.request.user)
        return queryset


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'appointments/detail.html'
    context_object_name = 'appointment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seizures'] = self.object.seizures.all()
        context['incidents'] = self.object.incidents.all()
        context['medications'] = self.object.medications.all()
        context['body_maps'] = self.object.body_maps.all()
        return context


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/create.html'
    success_url = reverse_lazy('appointment-list')


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/edit.html'
    success_url = reverse_lazy('appointment-list')


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/delete.html'
    success_url = reverse_lazy('appointment-list')


# API Views for Mobile App
class StaffAppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for staff to manage their appointments
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter appointments for the authenticated staff member"""
        if self.request.user.is_staff_member:
            return Appointment.objects.filter(assigned_staff=self.request.user).order_by('start_time')
        return Appointment.objects.none()

    @action(detail=True, methods=['post'])
    def start_visit(self, request, pk=None):
        """Start a visit by setting actual_start_time. Only allowed if appointment is today."""
        appointment = self.get_object()
        today = timezone.now().date()
        if appointment.start_time.date() != today:
            return Response(
                {'error': 'You can only start a visit on the day it is scheduled. Please try again on the correct date.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if appointment.actual_start_time:
            return Response(
                {'error': 'This visit has already been started. You cannot start it again.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.actual_start_time = timezone.now()
        appointment.status = 'in_progress'
        appointment.save()
        return Response({
            'message': 'Visit started successfully',
            'actual_start_time': appointment.actual_start_time
        })

    @action(detail=True, methods=['post'])
    def end_visit(self, request, pk=None):
        """End a visit by setting actual_end_time"""
        appointment = self.get_object()
        
        if not appointment.actual_start_time:
            return Response(
                {'error': 'Visit has not been started'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if appointment.actual_end_time:
            return Response(
                {'error': 'Visit has already been ended'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.actual_end_time = timezone.now()
        appointment.status = 'completed'
        appointment.save()
        
        return Response({
            'message': 'Visit ended successfully',
            'actual_end_time': appointment.actual_end_time,
            'duration_minutes': appointment.duration_minutes
        })

    @action(detail=True, methods=['post'])
    def update_checklist(self, request, pk=None):
        """Update checklist items for an appointment"""
        appointment = self.get_object()
        checklist_items = request.data.get('checklist_items', [])
        
        appointment.checklist_items = checklist_items
        appointment.save()
        
        return Response({
            'message': 'Checklist updated successfully',
            'checklist_items': appointment.checklist_items,
            'completion_percentage': appointment.checklist_completion_percentage
        })

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's appointments for the staff member"""
        today = timezone.now().date()
        queryset = self.get_queryset().filter(
            start_time__date=today
        ).order_by('start_time')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments for the staff member"""
        now = timezone.now()
        queryset = self.get_queryset().filter(
            start_time__gte=now
        ).order_by('start_time')[:10]  # Next 10 appointments
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """Get currently in-progress appointments for the staff member"""
        queryset = self.get_queryset().filter(
            status='in_progress'
        ).order_by('start_time')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def week(self, request):
        """Get this week's appointments for the staff member"""
        today = timezone.now().date()
        # Start of week (Monday)
        start_of_week = today - timedelta(days=today.weekday())
        # End of week (Sunday)
        end_of_week = start_of_week + timedelta(days=6)
        queryset = self.get_queryset().filter(
            start_time__date__gte=start_of_week,
            start_time__date__lte=end_of_week
        ).order_by('start_time')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Get all details for a single appointment, including client and notes"""
        appointment = self.get_object()
        from .serializers import AppointmentDetailSerializer
        serializer = AppointmentDetailSerializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def log_location(self, request, pk=None):
        """Log device location for visit (start, end, or deviation)"""
        appointment = self.get_object()
        log_type = request.data.get('log_type')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        if not all([log_type, latitude, longitude]):
            return Response({'error': 'log_type, latitude, and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return Response({'error': 'latitude and longitude must be numbers'}, status=status.HTTP_400_BAD_REQUEST)
        # Get client lat/lon
        client = appointment.client
        if not client.latitude or not client.longitude:
            return Response({'error': 'Client does not have latitude/longitude set'}, status=status.HTTP_400_BAD_REQUEST)
        # Haversine formula
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000  # meters
            phi1 = math.radians(lat1)
            phi2 = math.radians(lat2)
            dphi = math.radians(lat2 - lat1)
            dlambda = math.radians(lon2 - lon1)
            a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c
        distance = haversine(client.latitude, client.longitude, latitude, longitude)
        log = VisitLocationLog.objects.create(
            appointment=appointment,
            log_type=log_type,
            latitude=latitude,
            longitude=longitude,
            distance_from_client=distance
        )
        serializer = VisitLocationLogSerializer(log)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def location_logs(self, request, pk=None):
        """Get all location logs for a visit"""
        appointment = self.get_object()
        logs = appointment.location_logs.all().order_by('timestamp')
        serializer = VisitLocationLogSerializer(logs, many=True)
        return Response(serializer.data)


class SeizureViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing seizures
    """
    serializer_class = SeizureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter seizures for appointments assigned to the authenticated staff member"""
        if self.request.user.is_staff_member:
            return Seizure.objects.filter(appointment__assigned_staff=self.request.user).order_by('-start_time')
        return Seizure.objects.none()

    def perform_create(self, serializer):
        """Ensure the appointment belongs to the authenticated staff member"""
        appointment = serializer.validated_data['appointment']
        if appointment.assigned_staff != self.request.user:
            raise serializers.ValidationError("You can only add seizures to your own appointments")
        serializer.save()

    @action(detail=True, methods=['post'])
    def end_seizure(self, request, pk=None):
        """End a seizure by setting end_time"""
        seizure = self.get_object()
        
        if seizure.end_time:
            return Response(
                {'error': 'Seizure has already been ended'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        seizure.end_time = timezone.now()
        seizure.save()
        
        return Response({
            'message': 'Seizure ended successfully',
            'end_time': seizure.end_time,
            'duration_minutes': seizure.duration_minutes
        })


class IncidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing incidents
    """
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter incidents for appointments assigned to the authenticated staff member"""
        if self.request.user.is_staff_member:
            return Incident.objects.filter(appointment__assigned_staff=self.request.user).order_by('-time')
        return Incident.objects.none()

    def perform_create(self, serializer):
        """Ensure the appointment belongs to the authenticated staff member"""
        appointment = serializer.validated_data['appointment']
        if appointment.assigned_staff != self.request.user:
            raise serializers.ValidationError("You can only add incidents to your own appointments")
        serializer.save()

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent incidents (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        queryset = self.get_queryset().filter(
            time__gte=thirty_days_ago
        ).order_by('-time')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MedicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing medications
    """
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter medications for appointments assigned to the authenticated staff member"""
        if self.request.user.is_staff_member:
            return Medication.objects.filter(appointment__assigned_staff=self.request.user).order_by('-created_at')
        return Medication.objects.none()

    def perform_create(self, serializer):
        """Ensure the appointment belongs to the authenticated staff member"""
        appointment = serializer.validated_data['appointment']
        if appointment.assigned_staff != self.request.user:
            raise serializers.ValidationError("You can only add medications to your own appointments")
        serializer.save()

    @action(detail=False, methods=['get'])
    def by_appointment(self, request):
        """Get medications for a specific appointment"""
        appointment_id = request.query_params.get('appointment_id')
        if not appointment_id:
            return Response(
                {'error': 'appointment_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            staff = User.objects.get(user=self.request.user)
            queryset = self.get_queryset().filter(
                appointment_id=appointment_id,
                appointment__assigned_staff=staff
            )
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Appointment not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class BodyMapViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing body maps
    """
    serializer_class = BodyMapSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter body maps for appointments assigned to the authenticated staff member"""
        if self.request.user.is_staff_member:
            return BodyMap.objects.filter(appointment__assigned_staff=self.request.user).order_by('-date_recorded')
        return BodyMap.objects.none()

    def perform_create(self, serializer):
        """Ensure the appointment belongs to the authenticated staff member and set practitioner"""
        appointment = serializer.validated_data['appointment']
        if appointment.assigned_staff != self.request.user:
            raise serializers.ValidationError("You can only add body maps to your own appointments")
        
        # Set the practitioner to the current user
        serializer.save(practitioner=self.request.user)

    @action(detail=False, methods=['get'])
    def by_appointment(self, request):
        """Get body maps for a specific appointment"""
        appointment_id = request.query_params.get('appointment_id')
        if not appointment_id:
            return Response(
                {'error': 'appointment_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            staff = User.objects.get(user=self.request.user)
            queryset = self.get_queryset().filter(
                appointment_id=appointment_id,
                appointment__assigned_staff=staff
            )
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Appointment.DoesNotExist:
            return Response(
                {'error': 'Appointment not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class StaffDashboardAPIView(APIView):
    """
    API endpoint for staff dashboard data
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get dashboard data for the authenticated staff member"""
        if not request.user.is_staff_member:
            return Response(
                {'error': 'User is not a staff member'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        today = timezone.now().date()
        now = timezone.now()

        # Today's appointments
        today_appointments = Appointment.objects.filter(
            assigned_staff=request.user,
            start_time__date=today
        ).order_by('start_time')

        # In-progress appointments
        in_progress_appointments = Appointment.objects.filter(
            assigned_staff=request.user,
            status='in_progress'
        )

        # Upcoming appointments (next 7 days)
        upcoming_appointments = Appointment.objects.filter(
            assigned_staff=request.user,
            start_time__gte=now,
            start_time__lte=now + timedelta(days=7)
        ).order_by('start_time')

        # Recent incidents (last 7 days)
        recent_incidents = Incident.objects.filter(
            appointment__assigned_staff=request.user,
            time__gte=now - timedelta(days=7)
        ).order_by('-time')

        # Recent seizures (last 7 days)
        recent_seizures = Seizure.objects.filter(
            appointment__assigned_staff=request.user,
            start_time__gte=now - timedelta(days=7)
        ).order_by('-start_time')

        # Prepare user data
        user_data = {
            'id': request.user.id,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'full_name': request.user.full_name,
            'email': request.user.email,
            'phone': request.user.phone,
            'role': request.user.role,
            'role_display': request.user.get_role_display(),
            'is_active': request.user.is_active,
            'is_staff_member': request.user.is_staff_member,
        }

        dashboard_data = {
            'staff': user_data,
            'today_appointments': AppointmentSerializer(today_appointments, many=True).data,
            'in_progress_appointments': AppointmentSerializer(in_progress_appointments, many=True).data,
            'upcoming_appointments': AppointmentSerializer(upcoming_appointments, many=True).data,
            'recent_incidents': IncidentSerializer(recent_incidents, many=True).data,
            'recent_seizures': SeizureSerializer(recent_seizures, many=True).data,
            'stats': {
                'today_count': today_appointments.count(),
                'in_progress_count': in_progress_appointments.count(),
                'upcoming_count': upcoming_appointments.count(),
                'recent_incidents_count': recent_incidents.count(),
                'recent_seizures_count': recent_seizures.count(),
            }
        }

        return Response(dashboard_data)


@method_decorator(csrf_exempt, name='dispatch')
class MobileSyncAPIView(APIView):
    """
    API endpoint for mobile app data synchronization
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Sync data from mobile app"""
        if not request.user.is_staff_member:
            return Response(
                {'error': 'User is not a staff member'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        sync_data = request.data
        results = {
            'appointments_updated': 0,
            'seizures_created': 0,
            'incidents_created': 0,
            'medications_created': 0,
            'body_maps_created': 0,
            'errors': []
        }

        # Sync appointments
        if 'appointments' in sync_data:
            for appointment_data in sync_data['appointments']:
                try:
                    appointment = Appointment.objects.get(
                        id=appointment_data['id'],
                        assigned_staff=request.user
                    )
                    serializer = AppointmentSerializer(appointment, data=appointment_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        results['appointments_updated'] += 1
                    else:
                        results['errors'].append(f"Appointment {appointment_data['id']}: {serializer.errors}")
                except Appointment.DoesNotExist:
                    results['errors'].append(f"Appointment {appointment_data['id']}: Not found")

        # Sync seizures
        if 'seizures' in sync_data:
            for seizure_data in sync_data['seizures']:
                try:
                    serializer = SeizureSerializer(data=seizure_data)
                    if serializer.is_valid():
                        # Ensure appointment belongs to user
                        appointment = serializer.validated_data['appointment']
                        if appointment.assigned_staff == request.user:
                            serializer.save()
                            results['seizures_created'] += 1
                        else:
                            results['errors'].append(f"Seizure: Appointment not assigned to user")
                    else:
                        results['errors'].append(f"Seizure: {serializer.errors}")
                except Exception as e:
                    results['errors'].append(f"Seizure: {str(e)}")

        # Sync incidents
        if 'incidents' in sync_data:
            for incident_data in sync_data['incidents']:
                try:
                    serializer = IncidentSerializer(data=incident_data)
                    if serializer.is_valid():
                        # Ensure appointment belongs to user
                        appointment = serializer.validated_data['appointment']
                        if appointment.assigned_staff == request.user:
                            serializer.save()
                            results['incidents_created'] += 1
                        else:
                            results['errors'].append(f"Incident: Appointment not assigned to user")
                    else:
                        results['errors'].append(f"Incident: {serializer.errors}")
                except Exception as e:
                    results['errors'].append(f"Incident: {str(e)}")

        return Response(results)
