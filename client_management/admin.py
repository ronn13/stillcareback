from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'address', 'checklist_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at', 'checklist_count']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address Information', {
            'fields': ('address',)
        }),
        ('Care Plan', {
            'fields': ('care_checklist',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def checklist_count(self, obj):
        return len(obj.care_checklist) if obj.care_checklist else 0
    checklist_count.short_description = 'Checklist Items'
