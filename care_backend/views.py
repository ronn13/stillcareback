from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django import forms

from client_management.models import Client
from appointment_management.models import Appointment
from invoice_group.models import InvoiceGroup
from appointment_management.forms import AppointmentForm
from client_management.forms import ClientForm

User = get_user_model()

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'admin')

def dashboard(request):
    """Main dashboard view"""
    today = timezone.now().date()
    
    # Dashboard statistics
    total_clients = Client.objects.count()
    active_appointments = Appointment.objects.filter(
        Q(start_time__date__gte=today) & 
        Q(status='scheduled')
    ).count()
    pending_invoices = InvoiceGroup.objects.filter(
        client__isnull=False
    ).distinct().count()
    total_staff = User.objects.filter(is_staff_member=True, is_active=True).count()
    
    # Recent appointments
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_appointments = Appointment.objects.filter(
        start_time__gte=seven_days_ago
    ).order_by('-start_time')[:5]
    
    # Today's appointments
    today_appointments = Appointment.objects.filter(
        start_time__date=today
    ).order_by('start_time')[:5]
    
    context = {
        'total_clients': total_clients,
        'active_appointments': active_appointments,
        'pending_invoices': pending_invoices,
        'recent_appointments': recent_appointments,
        'today_appointments': today_appointments,
        'total_staff': total_staff,
    }
    
    return render(request, 'dashboard.html', context)

def clients_list(request):
    """List all clients"""
    search = request.GET.get('search', '')
    if search:
        clients = Client.objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        ).order_by('last_name', 'first_name')
    else:
        clients = Client.objects.all().order_by('last_name', 'first_name')
    
    context = {
        'clients': clients,
        'search': search,
    }
    return render(request, 'clients/list.html', context)

def client_create(request):
    """Create a new client"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client created successfully!')
            return redirect('client_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientForm()
    context = {
        'form': form,
    }
    return render(request, 'clients/create.html', context)

def client_edit(request, client_id):
    """Edit a client"""
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully!')
            return redirect('client_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClientForm(instance=client)
    context = {
        'form': form,
        'client': client,
    }
    return render(request, 'clients/edit.html', context)

def client_delete(request, client_id):
    """Delete a client"""
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client deleted successfully!')
        return redirect('client_list')
    
    context = {'client': client}
    return render(request, 'clients/delete.html', context)

def client_detail(request, client_id):
    """View client details"""
    client = get_object_or_404(Client, id=client_id)
    appointments = Appointment.objects.filter(client=client).order_by('-start_time')
    invoices = InvoiceGroup.objects.filter(client=client).order_by('-created_at')
    
    context = {
        'client': client,
        'appointments': appointments,
        'invoices': invoices,
    }
    return render(request, 'clients/detail.html', context)

def appointments_list(request):
    """List all appointments"""
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    appointments = Appointment.objects.all().order_by('-start_time')
    
    if search:
        appointments = appointments.filter(
            Q(title__icontains=search) |
            Q(client__first_name__icontains=search) |
            Q(client__last_name__icontains=search)
        )
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'search': search,
        'status_filter': status_filter,
    }
    return render(request, 'appointments/list.html', context)

def appointment_create(request):
    """Create a new appointment"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            # Automatically create repeated appointments if frequency is set and status is not completed
            freq = appointment.frequency
            status = appointment.status
            if freq and status != 'completed':
                occurrences = 5
                delta = None
                if freq == 'daily':
                    delta = timedelta(days=1)
                elif freq == 'weekly':
                    delta = timedelta(weeks=1)
                elif freq == 'monthly':
                    # For monthly, add 30 days as a simple approximation
                    delta = timedelta(days=30)
                if delta:
                    start = appointment.start_time
                    end = appointment.end_time
                    for i in range(1, occurrences+1):
                        new_start = start + delta * i
                        new_end = end + delta * i
                        Appointment.objects.create(
                            title=appointment.title,
                            description=appointment.description,
                            client=appointment.client,
                            start_time=new_start,
                            end_time=new_end,
                            status=appointment.status,
                            frequency=appointment.frequency,
                        )
            messages.success(request, 'Appointment created successfully!')
            return redirect('appointment_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentForm()
    context = {
        'form': form,
    }
    return render(request, 'appointments/create.html', context)

def appointment_edit(request, appointment_id):
    """Edit an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('appointment_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentForm(instance=appointment)
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'appointments/edit.html', context)

def appointment_delete(request, appointment_id):
    """Delete an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('appointment_list')
    
    context = {'appointment': appointment}
    return render(request, 'appointments/delete.html', context)

def appointment_detail(request, appointment_id):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    notes = appointment.notes.all().order_by('-created_at')
    context = {
        'appointment': appointment,
        'notes': notes,
    }
    return render(request, 'appointments/detail.html', context)

def invoices_list(request):
    """List all invoice groups"""
    search = request.GET.get('search', '')
    
    invoices = InvoiceGroup.objects.all().order_by('-created_at')
    
    if search:
        invoices = invoices.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    context = {
        'invoices': invoices,
        'search': search,
    }
    return render(request, 'invoices/list.html', context)

def invoice_create(request):
    """Create a new invoice group"""
    if request.method == 'POST':
        try:
            client = get_object_or_404(Client, id=request.POST['client'])
            invoice = InvoiceGroup.objects.create(
                name=request.POST['name'],
                rate_per_hour=request.POST.get('rate_per_hour', 0),
                client=client,
            )
            messages.success(request, 'Invoice group created successfully!')
            return redirect('invoice_list')
        except Exception as e:
            messages.error(request, f'Error creating invoice group: {str(e)}')
    
    context = {
        'clients': Client.objects.all().order_by('last_name', 'first_name'),
    }
    return render(request, 'invoices/create.html', context)

def invoice_edit(request, invoice_id):
    """Edit an invoice group"""
    invoice = get_object_or_404(InvoiceGroup, id=invoice_id)
    
    if request.method == 'POST':
        try:
            client = get_object_or_404(Client, id=request.POST['client'])
            invoice.name = request.POST['name']
            invoice.rate_per_hour = request.POST.get('rate_per_hour', 0)
            invoice.client = client
            invoice.save()
            
            messages.success(request, 'Invoice group updated successfully!')
            return redirect('invoice_list')
        except Exception as e:
            messages.error(request, f'Error updating invoice group: {str(e)}')
    
    context = {
        'invoice': invoice,
        'clients': Client.objects.all().order_by('last_name', 'first_name'),
    }
    return render(request, 'invoices/edit.html', context)

def invoice_delete(request, invoice_id):
    """Delete an invoice group"""
    invoice = get_object_or_404(InvoiceGroup, id=invoice_id)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Invoice group deleted successfully!')
        return redirect('invoice_list')
    
    context = {'invoice': invoice}
    return render(request, 'invoices/delete.html', context)

def invoice_detail(request, invoice_id):
    """View invoice details"""
    invoice = get_object_or_404(InvoiceGroup, id=invoice_id)
    
    context = {
        'invoice': invoice,
    }
    return render(request, 'invoices/detail.html', context)

# API views (keeping for potential future use)
@api_view(['GET'])
def dashboard_stats(request):
    """Get dashboard statistics"""
    today = timezone.now().date()
    
    # Total clients
    total_clients = Client.objects.count()
    
    # Active appointments (scheduled for today or future)
    active_appointments = Appointment.objects.filter(
        Q(start_time__date__gte=today) & 
        Q(status='scheduled')
    ).count()
    
    # Pending invoices (invoice groups with clients)
    pending_invoices = InvoiceGroup.objects.filter(
        client__isnull=False
    ).distinct().count()
    
    return Response({
        'total_clients': total_clients,
        'active_appointments': active_appointments,
        'pending_invoices': pending_invoices,
    }) 

# User Management Views
@login_required
@user_passes_test(is_admin)
def users_list(request):
    """List all users"""
    search = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    
    users = User.objects.all().order_by('username')
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    context = {
        'users': users,
        'search': search,
        'role_filter': role_filter,
    }
    return render(request, 'users/list.html', context)

@login_required
@user_passes_test(is_admin)
def user_create(request):
    """Create a new user"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = request.POST.get('role', 'nurse')
            user.is_staff_member = request.POST.get('is_staff_member') == 'on'
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.phone = request.POST.get('phone', '')
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect('user_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/create.html', context)

@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    """View user details"""
    user = get_object_or_404(User, id=user_id)
    appointments = Appointment.objects.filter(assigned_staff=user).order_by('-start_time')
    
    context = {
        'user_detail': user,
        'appointments': appointments,
    }
    return render(request, 'users/detail.html', context)

@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    """Edit a user"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.role = request.POST.get('role', 'nurse')
        user.is_staff_member = request.POST.get('is_staff_member') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        
        if request.POST.get('password1') and request.POST.get('password1') == request.POST.get('password2'):
            user.set_password(request.POST.get('password1'))
        
        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('user_list')
    
    context = {
        'user_detail': user,
    }
    return render(request, 'users/edit.html', context)

@login_required
@user_passes_test(is_admin)
def user_delete(request, user_id):
    """Delete a user"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    
    context = {'user_detail': user}
    return render(request, 'users/delete.html', context) 