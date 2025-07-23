from django.db import models

class Client(models.Model):
    CHECKLIST_CHOICES = [
        ('basic_care', 'Basic Care'),
        ('medication_management', 'Medication Management'),
        ('wound_care', 'Wound Care'),
        ('physical_therapy', 'Physical Therapy'),
        ('nursing_care', 'Nursing Care'),
        ('social_work', 'Social Work'),
        ('nutrition', 'Nutrition'),
        ('hygiene', 'Hygiene'),
        ('mobility', 'Mobility Assistance'),
        ('monitoring', 'Vital Signs Monitoring'),
        ('education', 'Patient Education'),
        ('family_support', 'Family Support'),
        ('emergency_prep', 'Emergency Preparedness'),
        ('equipment', 'Medical Equipment'),
        ('transportation', 'Transportation'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    latitude = models.FloatField(blank=True, null=True, help_text="Latitude of the client's residence")
    longitude = models.FloatField(blank=True, null=True, help_text="Longitude of the client's residence")

    # Client care checklist
    care_checklist = models.JSONField(
        default=list,
        help_text="List of care items required for this client"
    )
    
    # Note: Invoice relationship is now handled via many-to-many in InvoiceGroup model
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_address(self):
        return self.address

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['last_name', 'first_name']
