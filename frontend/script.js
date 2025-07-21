// StillCare Healthcare Frontend JavaScript

// API Base URL - Update this to match your Django backend
const API_BASE_URL = 'http://localhost:8000/api';

// Global variables
let clients = [];
let appointments = [];
let visits = [];
let invoices = [];

// Checklist options for clients
const CHECKLIST_OPTIONS = [
    { value: 'basic_care', label: 'Basic Care' },
    { value: 'medication_management', label: 'Medication Management' },
    { value: 'wound_care', label: 'Wound Care' },
    { value: 'physical_therapy', label: 'Physical Therapy' },
    { value: 'nursing_care', label: 'Nursing Care' },
    { value: 'social_work', label: 'Social Work' },
    { value: 'nutrition', label: 'Nutrition' },
    { value: 'hygiene', label: 'Hygiene' },
    { value: 'mobility', label: 'Mobility Assistance' },
    { value: 'monitoring', label: 'Vital Signs Monitoring' },
    { value: 'education', label: 'Patient Education' },
    { value: 'family_support', label: 'Family Support' },
    { value: 'emergency_prep', label: 'Emergency Preparedness' },
    { value: 'equipment', label: 'Medical Equipment' },
    { value: 'transportation', label: 'Transportation' }
];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
    loadClients();
    loadAppointments();
    loadVisits();
    loadInvoices();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Repeats checkbox for appointments
    document.getElementById('repeats').addEventListener('change', function() {
        const frequencyGroup = document.getElementById('frequencyGroup');
        frequencyGroup.style.display = this.checked ? 'block' : 'none';
    });

    // Visit appointment change
    document.getElementById('visitAppointment').addEventListener('change', function() {
        loadVisitChecklist();
    });
}

// ==================== DASHBOARD ====================

async function loadDashboard() {
    try {
        // Load dashboard statistics
        const stats = await fetch(`${API_BASE_URL}/dashboard/`).then(r => r.json());
        
        document.getElementById('totalClients').textContent = stats.total_clients || 0;
        document.getElementById('activeAppointments').textContent = stats.active_appointments || 0;
        document.getElementById('todayVisits').textContent = stats.today_visits || 0;
        document.getElementById('pendingInvoices').textContent = stats.pending_invoices || 0;

        // Load recent appointments
        loadRecentAppointments();
        loadTodayVisits();
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    }
}

async function loadRecentAppointments() {
    try {
        const response = await fetch(`${API_BASE_URL}/appointments/recent/`);
        const data = await response.json();
        
        const container = document.getElementById('recentAppointments');
        container.innerHTML = '';
        
        data.slice(0, 5).forEach(appointment => {
            const item = document.createElement('div');
            item.className = 'list-group-item d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <div>
                    <strong>${appointment.title}</strong><br>
                    <small class="text-muted">${appointment.client_name}</small>
                </div>
                <span class="badge bg-primary">${formatDateTime(appointment.start_time)}</span>
            `;
            container.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading recent appointments:', error);
    }
}

async function loadTodayVisits() {
    try {
        const response = await fetch(`${API_BASE_URL}/visits/today/`);
        const data = await response.json();
        
        const container = document.getElementById('todayVisitsList');
        container.innerHTML = '';
        
        data.slice(0, 5).forEach(visit => {
            const item = document.createElement('div');
            item.className = 'list-group-item d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <div>
                    <strong>${visit.client_name}</strong><br>
                    <small class="text-muted">${visit.assigned_staff || 'Unassigned'}</small>
                </div>
                <span class="badge bg-${getStatusColor(visit.status)}">${visit.status}</span>
            `;
            container.appendChild(item);
        });
    } catch (error) {
        console.error('Error loading today\'s visits:', error);
    }
}

// ==================== CLIENTS ====================

async function loadClients() {
    try {
        const response = await fetch(`${API_BASE_URL}/clients/`);
        clients = await response.json();
        renderClientsTable();
    } catch (error) {
        console.error('Error loading clients:', error);
        showAlert('Error loading clients', 'danger');
    }
}

function renderClientsTable() {
    const tbody = document.getElementById('clientsTableBody');
    tbody.innerHTML = '';
    
    clients.forEach(client => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${client.first_name} ${client.last_name}</strong></td>
            <td>${client.email || '-'}</td>
            <td>${client.phone || '-'}</td>
            <td>${client.address}</td>
            <td><span class="badge bg-info">${client.care_checklist ? client.care_checklist.length : 0} items</span></td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editClient(${client.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteClient(${client.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function openClientModal(clientId = null) {
    const modal = new bootstrap.Modal(document.getElementById('clientModal'));
    const title = document.getElementById('clientModalTitle');
    const form = document.getElementById('clientForm');
    
    if (clientId) {
        title.textContent = 'Edit Client';
        const client = clients.find(c => c.id === clientId);
        if (client) {
            document.getElementById('clientId').value = client.id;
            document.getElementById('firstName').value = client.first_name;
            document.getElementById('lastName').value = client.last_name;
            document.getElementById('email').value = client.email || '';
            document.getElementById('phone').value = client.phone || '';
            document.getElementById('address').value = client.address;
            renderChecklist(client.care_checklist || []);
        }
    } else {
        title.textContent = 'Add New Client';
        form.reset();
        document.getElementById('clientId').value = '';
        renderChecklist([]);
    }
    
    modal.show();
}

function renderChecklist(selectedItems) {
    const container = document.getElementById('careChecklist');
    container.innerHTML = '';
    
    CHECKLIST_OPTIONS.forEach(option => {
        const item = document.createElement('div');
        item.className = 'checklist-item';
        const isSelected = selectedItems.includes(option.value);
        
        item.innerHTML = `
            <input type="checkbox" id="checklist_${option.value}" value="${option.value}" ${isSelected ? 'checked' : ''}>
            <label for="checklist_${option.value}">${option.label}</label>
        `;
        
        if (isSelected) {
            item.classList.add('selected');
        }
        
        item.addEventListener('click', function(e) {
            if (e.target.type !== 'checkbox') {
                const checkbox = this.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
            }
            
            if (this.querySelector('input[type="checkbox"]').checked) {
                this.classList.add('selected');
            } else {
                this.classList.remove('selected');
            }
        });
        
        container.appendChild(item);
    });
}

async function saveClient() {
    const form = document.getElementById('clientForm');
    const clientId = document.getElementById('clientId').value;
    
    // Get selected checklist items
    const selectedItems = Array.from(document.querySelectorAll('#careChecklist input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    const clientData = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value,
        care_checklist: selectedItems
    };
    
    try {
        const url = clientId ? `${API_BASE_URL}/clients/${clientId}/` : `${API_BASE_URL}/clients/`;
        const method = clientId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clientData)
        });
        
        if (response.ok) {
            showAlert(clientId ? 'Client updated successfully' : 'Client created successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('clientModal')).hide();
            loadClients();
            loadDashboard();
        } else {
            throw new Error('Failed to save client');
        }
    } catch (error) {
        console.error('Error saving client:', error);
        showAlert('Error saving client', 'danger');
    }
}

async function deleteClient(clientId) {
    if (!confirm('Are you sure you want to delete this client?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/clients/${clientId}/`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Client deleted successfully', 'success');
            loadClients();
            loadDashboard();
        } else {
            throw new Error('Failed to delete client');
        }
    } catch (error) {
        console.error('Error deleting client:', error);
        showAlert('Error deleting client', 'danger');
    }
}

// ==================== APPOINTMENTS ====================

async function loadAppointments() {
    try {
        const response = await fetch(`${API_BASE_URL}/appointments/`);
        appointments = await response.json();
        renderAppointmentsTable();
        populateClientSelect();
    } catch (error) {
        console.error('Error loading appointments:', error);
        showAlert('Error loading appointments', 'danger');
    }
}

function renderAppointmentsTable() {
    const tbody = document.getElementById('appointmentsTableBody');
    tbody.innerHTML = '';
    
    appointments.forEach(appointment => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${appointment.title}</strong></td>
            <td>${appointment.client_name}</td>
            <td>${formatDateTime(appointment.start_time)}</td>
            <td>${formatDateTime(appointment.end_time)}</td>
            <td><span class="badge bg-${getStatusColor(appointment.status)}">${appointment.status}</span></td>
            <td>${appointment.repeats ? `<span class="badge bg-info">${appointment.frequency || 'Custom'}</span>` : '-'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editAppointment(${appointment.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteAppointment(${appointment.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function populateClientSelect() {
    const select = document.getElementById('appointmentClient');
    select.innerHTML = '<option value="">Select Client</option>';
    
    clients.forEach(client => {
        const option = document.createElement('option');
        option.value = client.id;
        option.textContent = `${client.first_name} ${client.last_name}`;
        select.appendChild(option);
    });
}

function openAppointmentModal(appointmentId = null) {
    const modal = new bootstrap.Modal(document.getElementById('appointmentModal'));
    const title = document.getElementById('appointmentModalTitle');
    const form = document.getElementById('appointmentForm');
    
    if (appointmentId) {
        title.textContent = 'Edit Appointment';
        const appointment = appointments.find(a => a.id === appointmentId);
        if (appointment) {
            document.getElementById('appointmentId').value = appointment.id;
            document.getElementById('appointmentTitle').value = appointment.title;
            document.getElementById('appointmentClient').value = appointment.client;
            document.getElementById('startTime').value = formatDateTimeForInput(appointment.start_time);
            document.getElementById('endTime').value = formatDateTimeForInput(appointment.end_time);
            document.getElementById('appointmentDescription').value = appointment.description || '';
            document.getElementById('appointmentStatus').value = appointment.status;
            document.getElementById('repeats').checked = appointment.repeats;
            document.getElementById('frequency').value = appointment.frequency || '';
            document.getElementById('frequencyGroup').style.display = appointment.repeats ? 'block' : 'none';
        }
    } else {
        title.textContent = 'Schedule Appointment';
        form.reset();
        document.getElementById('appointmentId').value = '';
        document.getElementById('frequencyGroup').style.display = 'none';
    }
    
    modal.show();
}

async function saveAppointment() {
    const form = document.getElementById('appointmentForm');
    const appointmentId = document.getElementById('appointmentId').value;
    
    const appointmentData = {
        title: document.getElementById('appointmentTitle').value,
        client: document.getElementById('appointmentClient').value,
        start_time: document.getElementById('startTime').value,
        end_time: document.getElementById('endTime').value,
        description: document.getElementById('appointmentDescription').value,
        status: document.getElementById('appointmentStatus').value,
        repeats: document.getElementById('repeats').checked,
        frequency: document.getElementById('repeats').checked ? document.getElementById('frequency').value : null
    };
    
    try {
        const url = appointmentId ? `${API_BASE_URL}/appointments/${appointmentId}/` : `${API_BASE_URL}/appointments/`;
        const method = appointmentId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(appointmentData)
        });
        
        if (response.ok) {
            showAlert(appointmentId ? 'Appointment updated successfully' : 'Appointment created successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('appointmentModal')).hide();
            loadAppointments();
            loadDashboard();
        } else {
            throw new Error('Failed to save appointment');
        }
    } catch (error) {
        console.error('Error saving appointment:', error);
        showAlert('Error saving appointment', 'danger');
    }
}

async function deleteAppointment(appointmentId) {
    if (!confirm('Are you sure you want to delete this appointment?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Appointment deleted successfully', 'success');
            loadAppointments();
            loadDashboard();
        } else {
            throw new Error('Failed to delete appointment');
        }
    } catch (error) {
        console.error('Error deleting appointment:', error);
        showAlert('Error deleting appointment', 'danger');
    }
}

// ==================== VISITS ====================

async function loadVisits() {
    try {
        const response = await fetch(`${API_BASE_URL}/visits/`);
        visits = await response.json();
        renderVisitsTable();
        populateAppointmentSelect();
    } catch (error) {
        console.error('Error loading visits:', error);
        showAlert('Error loading visits', 'danger');
    }
}

function renderVisitsTable() {
    const tbody = document.getElementById('visitsTableBody');
    tbody.innerHTML = '';
    
    visits.forEach(visit => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${visit.client_name}</strong></td>
            <td><span class="badge bg-${getStatusColor(visit.status)}">${visit.status}</span></td>
            <td>${visit.actual_start_time ? formatDateTime(visit.actual_start_time) : '-'}</td>
            <td>${visit.actual_end_time ? formatDateTime(visit.actual_end_time) : '-'}</td>
            <td>${visit.duration_minutes ? `${visit.duration_minutes} min` : '-'}</td>
            <td>${visit.assigned_staff || '-'}</td>
            <td>
                <div class="progress" style="width: 100px;">
                    <div class="progress-bar" style="width: ${visit.checklist_completion_percentage || 0}%"></div>
                </div>
                <small>${Math.round(visit.checklist_completion_percentage || 0)}%</small>
            </td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editVisit(${visit.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteVisit(${visit.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function populateAppointmentSelect() {
    const select = document.getElementById('visitAppointment');
    select.innerHTML = '<option value="">Select Appointment</option>';
    
    appointments.forEach(appointment => {
        const option = document.createElement('option');
        option.value = appointment.id;
        option.textContent = `${appointment.title} - ${appointment.client_name} (${formatDateTime(appointment.start_time)})`;
        select.appendChild(option);
    });
}

function openVisitModal(visitId = null) {
    const modal = new bootstrap.Modal(document.getElementById('visitModal'));
    const title = document.getElementById('visitModalTitle');
    const form = document.getElementById('visitForm');
    
    if (visitId) {
        title.textContent = 'Edit Visit';
        const visit = visits.find(v => v.id === visitId);
        if (visit) {
            document.getElementById('visitId').value = visit.id;
            document.getElementById('visitAppointment').value = visit.appointment;
            document.getElementById('visitStatus').value = visit.status;
            document.getElementById('actualStartTime').value = visit.actual_start_time ? formatDateTimeForInput(visit.actual_start_time) : '';
            document.getElementById('actualEndTime').value = visit.actual_end_time ? formatDateTimeForInput(visit.actual_end_time) : '';
            document.getElementById('assignedStaff').value = visit.assigned_staff || '';
            document.getElementById('visitNotes').value = visit.visit_notes || '';
            renderVisitChecklist(visit.checklist_items || []);
        }
    } else {
        title.textContent = 'Record Visit';
        form.reset();
        document.getElementById('visitId').value = '';
        renderVisitChecklist([]);
    }
    
    modal.show();
}

function loadVisitChecklist() {
    const appointmentId = document.getElementById('visitAppointment').value;
    if (appointmentId) {
        const appointment = appointments.find(a => a.id == appointmentId);
        if (appointment) {
            const client = clients.find(c => c.id == appointment.client);
            if (client) {
                renderVisitChecklist(client.care_checklist || []);
            }
        }
    } else {
        renderVisitChecklist([]);
    }
}

function renderVisitChecklist(selectedItems) {
    const container = document.getElementById('visitChecklist');
    container.innerHTML = '';
    
    CHECKLIST_OPTIONS.forEach(option => {
        const item = document.createElement('div');
        item.className = 'checklist-item';
        const isSelected = selectedItems.includes(option.value);
        
        item.innerHTML = `
            <input type="checkbox" id="visit_checklist_${option.value}" value="${option.value}" ${isSelected ? 'checked' : ''}>
            <label for="visit_checklist_${option.value}">${option.label}</label>
        `;
        
        if (isSelected) {
            item.classList.add('selected');
        }
        
        item.addEventListener('click', function(e) {
            if (e.target.type !== 'checkbox') {
                const checkbox = this.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
            }
            
            if (this.querySelector('input[type="checkbox"]').checked) {
                this.classList.add('selected');
            } else {
                this.classList.remove('selected');
            }
        });
        
        container.appendChild(item);
    });
}

async function saveVisit() {
    const form = document.getElementById('visitForm');
    const visitId = document.getElementById('visitId').value;
    
    // Get selected checklist items
    const selectedItems = Array.from(document.querySelectorAll('#visitChecklist input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    const visitData = {
        appointment: document.getElementById('visitAppointment').value,
        status: document.getElementById('visitStatus').value,
        actual_start_time: document.getElementById('actualStartTime').value || null,
        actual_end_time: document.getElementById('actualEndTime').value || null,
        assigned_staff: document.getElementById('assignedStaff').value,
        visit_notes: document.getElementById('visitNotes').value,
        checklist_items: selectedItems
    };
    
    try {
        const url = visitId ? `${API_BASE_URL}/visits/${visitId}/` : `${API_BASE_URL}/visits/`;
        const method = visitId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(visitData)
        });
        
        if (response.ok) {
            showAlert(visitId ? 'Visit updated successfully' : 'Visit created successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('visitModal')).hide();
            loadVisits();
            loadDashboard();
        } else {
            throw new Error('Failed to save visit');
        }
    } catch (error) {
        console.error('Error saving visit:', error);
        showAlert('Error saving visit', 'danger');
    }
}

async function deleteVisit(visitId) {
    if (!confirm('Are you sure you want to delete this visit?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/visits/${visitId}/`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Visit deleted successfully', 'success');
            loadVisits();
            loadDashboard();
        } else {
            throw new Error('Failed to delete visit');
        }
    } catch (error) {
        console.error('Error deleting visit:', error);
        showAlert('Error deleting visit', 'danger');
    }
}

// ==================== INVOICES ====================

async function loadInvoices() {
    try {
        const response = await fetch(`${API_BASE_URL}/invoices/`);
        invoices = await response.json();
        renderInvoicesTable();
    } catch (error) {
        console.error('Error loading invoices:', error);
        showAlert('Error loading invoices', 'danger');
    }
}

function renderInvoicesTable() {
    const tbody = document.getElementById('invoicesTableBody');
    tbody.innerHTML = '';
    
    invoices.forEach(invoice => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${invoice.name}</strong></td>
            <td>${invoice.description || '-'}</td>
            <td><span class="badge bg-info">${invoice.clients_count || 0} clients</span></td>
            <td>${formatDateTime(invoice.created_at)}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editInvoice(${invoice.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteInvoice(${invoice.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function openInvoiceModal(invoiceId = null) {
    const modal = new bootstrap.Modal(document.getElementById('invoiceModal'));
    const title = document.getElementById('invoiceModalTitle');
    const form = document.getElementById('invoiceForm');
    
    if (invoiceId) {
        title.textContent = 'Edit Invoice Group';
        const invoice = invoices.find(i => i.id === invoiceId);
        if (invoice) {
            document.getElementById('invoiceId').value = invoice.id;
            document.getElementById('invoiceName').value = invoice.name;
            document.getElementById('invoiceDescription').value = invoice.description || '';
        }
    } else {
        title.textContent = 'Create Invoice Group';
        form.reset();
        document.getElementById('invoiceId').value = '';
    }
    
    modal.show();
}

async function saveInvoice() {
    const form = document.getElementById('invoiceForm');
    const invoiceId = document.getElementById('invoiceId').value;
    
    const invoiceData = {
        name: document.getElementById('invoiceName').value,
        description: document.getElementById('invoiceDescription').value
    };
    
    try {
        const url = invoiceId ? `${API_BASE_URL}/invoices/${invoiceId}/` : `${API_BASE_URL}/invoices/`;
        const method = invoiceId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(invoiceData)
        });
        
        if (response.ok) {
            showAlert(invoiceId ? 'Invoice group updated successfully' : 'Invoice group created successfully', 'success');
            bootstrap.Modal.getInstance(document.getElementById('invoiceModal')).hide();
            loadInvoices();
            loadDashboard();
        } else {
            throw new Error('Failed to save invoice group');
        }
    } catch (error) {
        console.error('Error saving invoice group:', error);
        showAlert('Error saving invoice group', 'danger');
    }
}

async function deleteInvoice(invoiceId) {
    if (!confirm('Are you sure you want to delete this invoice group?')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/invoices/${invoiceId}/`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showAlert('Invoice group deleted successfully', 'success');
            loadInvoices();
            loadDashboard();
        } else {
            throw new Error('Failed to delete invoice group');
        }
    } catch (error) {
        console.error('Error deleting invoice group:', error);
        showAlert('Error deleting invoice group', 'danger');
    }
}

// ==================== UTILITY FUNCTIONS ====================

function formatDateTime(dateTimeString) {
    if (!dateTimeString) return '-';
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDateTimeForInput(dateTimeString) {
    if (!dateTimeString) return '';
    const date = new Date(dateTimeString);
    return date.toISOString().slice(0, 16);
}

function getStatusColor(status) {
    switch (status) {
        case 'completed':
        case 'scheduled':
            return 'success';
        case 'in_progress':
            return 'info';
        case 'cancelled':
        case 'no_show':
            return 'danger';
        default:
            return 'secondary';
    }
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Edit functions (placeholder implementations)
function editClient(id) {
    openClientModal(id);
}

function editAppointment(id) {
    openAppointmentModal(id);
}

function editVisit(id) {
    openVisitModal(id);
}

function editInvoice(id) {
    openInvoiceModal(id);
} 