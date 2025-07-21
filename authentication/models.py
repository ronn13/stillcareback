from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser
    """
    ROLE_CHOICES = [
        ('nurse', 'Nurse'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='nurse',
        help_text="User role in the system"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_staff_member = models.BooleanField(
        default=True,
        help_text="Whether this user is a staff member"
    )
    login_code = models.CharField(
        max_length=6,
        unique=True,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{6}$',
                message='Login code must be exactly 6 digits.',
                code='invalid_login_code'
            ),
        ],
        help_text="6-digit code for app login (optional)"
    )
    biometric_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique biometric identifier for fingerprint/face recognition (optional)"
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    @property
    def full_name(self):
        """Get the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_nurse(self):
        """Check if user is a nurse"""
        return self.role == 'nurse'
    
    @property
    def is_admin_user(self):
        """Check if user is an admin"""
        return self.role == 'admin'
    
    @property
    def has_biometric(self):
        """Check if user has biometric authentication enabled"""
        return bool(self.biometric_id)
    
    @property
    def has_login_code(self):
        """Check if user has login code authentication enabled"""
        return bool(self.login_code)
    
    def clean(self):
        """Custom validation for the model"""
        super().clean()
        if self.login_code and len(self.login_code) != 6:
            raise ValidationError({'login_code': 'Login code must be exactly 6 digits.'})
