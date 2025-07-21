from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from appointment_management.models import Appointment
from django.contrib.auth.decorators import login_required

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