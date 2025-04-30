from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Asset(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('RETIRED', 'Retired'),
    ]
    
    CONDITION_CHOICES = [
        ('NEW', 'New'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('POOR', 'Poor'),
    ]

    registration_date = models.DateTimeField(default=timezone.now)
    asset_id = models.CharField(max_length=50, unique=True)
    asset_type = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    operating_system = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    ram = models.IntegerField(validators=[MinValueValidator(0)])
    storage = models.IntegerField(validators=[MinValueValidator(0)])
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    assignee = models.EmailField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='NEW')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asset_id} - {self.make} {self.model}"

    class Meta:
        ordering = ['-registration_date']
