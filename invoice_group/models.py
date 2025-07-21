from django.db import models
from client_management.models import Client
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class InvoiceGroup(models.Model):
    # Basic invoice information
    name = models.CharField(max_length=100, help_text="Invoice title/description")
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    
    # Client relationship
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='invoice_group')
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Financial information
    def __str__(self):
        return f"Invoice {self.name}"

    def get_client_names(self):
        """Get comma-separated list of client names"""
        return self.client.full_name if self.client else ""

    class Meta:
        verbose_name = "Invoice Group"
        verbose_name_plural = "Invoice Groups"
