from django.contrib import admin
from .models import InvoiceGroup

@admin.register(InvoiceGroup)
class InvoiceGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'rate_per_hour']
    list_filter = []
    search_fields = ['name', 'client__full_name']
    
    