from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff_member', 'login_code', 'biometric_id', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff_member', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'login_code', 'biometric_id')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('App Authentication', {'fields': ('login_code', 'biometric_id')}),
        ('Role & Permissions', {
            'fields': ('role', 'is_staff_member', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_staff_member', 'login_code', 'biometric_id'),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
