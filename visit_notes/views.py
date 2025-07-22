from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from appointment_management.models import Appointment
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import NoteSerializer

@login_required
def note_create(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.appointment = appointment
            note.uploaded_by = request.user
            note.save()
            messages.success(request, 'Note added successfully!')
            return redirect('appointment_detail', appointment_id=appointment.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm()
    return render(request, 'visit_notes/create.html', {'form': form, 'appointment': appointment})

@login_required
def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('appointment_detail', appointment_id=note.appointment.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm(instance=note)
    return render(request, 'visit_notes/edit.html', {'form': form, 'note': note})

@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    appointment_id = note.appointment.id
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('appointment_detail', appointment_id=appointment_id)
    return render(request, 'visit_notes/delete.html', {'note': note})

@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'visit_notes/detail.html', {'note': note})

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all().order_by('-created_at')
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        appointment_id = self.request.query_params.get('appointment_id')
        if appointment_id:
            queryset = queryset.filter(appointment_id=appointment_id)
        return queryset

    @action(detail=False, methods=['get'])
    def by_appointment(self, request):
        appointment_id = request.query_params.get('appointment_id')
        if not appointment_id:
            return Response({'error': 'appointment_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        notes = self.get_queryset().filter(appointment_id=appointment_id)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data) 