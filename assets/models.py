from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Asset(models.Model):
    STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned'),
        ('AVAILABLE', 'Available'),
        ('IN_REPAIR', 'In-repair'),
        ('RETIRED', 'Retired'),
    ]
    
    CONDITION_CHOICES = [
        ('WORKING', 'Working'),
        ('SOFTWARE_ISSUE', 'Software-issue'),
        ('HARDWARE_ISSUE', 'Hardware-issue'),
        ('DAMAGED', 'Damaged'),
    ]

    ASSET_TYPE_CHOICES = [
        ('LAPTOP', 'Laptop'),
        ('DESKTOP', 'Desktop'),
        ('MOBILE', 'Mobile'),
        ('TABLET', 'Tablet'),
        ('PRINTER', 'Printer'),
        ('SCANNER', 'Scanner'),
        ('PROJECTOR', 'Projector'),
        ('SERVER', 'Server'),
        ('NETWORK_DEVICE', 'Network Device'),
        ('MONITOR', 'Monitor'),
        ('SCREEN', 'Screen'),
        ('TV', 'TV'),
        ('ROBOTS', 'Robots'),
        ('UPS', 'UPS'),
        ('EXTERNAL_DRIVE', 'External Drive'),
        ('OTHER', 'Other'),
    ]

    OS_CHOICES = [
        ('WINDOWS', 'Windows'),
        ('MACOS', 'macOS'),
        ('LINUX', 'Linux'),
        ('ANDROID', 'Android'),
        ('IOS', 'iOS'),
        ('CHROMEOS', 'ChromeOS'),
        ('HYPEROS', 'HyperOS'),
        ('OTHER', 'Other'),
    ]

    UNIT_CHOICES = [
        ('MB', 'MB'),
        ('GB', 'GB'),
        ('TB', 'TB'),
    ]

    registration_date = models.DateTimeField(default=timezone.now)
    asset_id = models.CharField(max_length=50, unique=True)
    asset_type = models.CharField(max_length=100, choices=ASSET_TYPE_CHOICES)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    operating_system = models.CharField(max_length=100, choices=OS_CHOICES)
    processor = models.CharField(max_length=100, blank=True)
    ram = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    ram_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='GB')
    storage = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    storage_unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default='GB')
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    assignee = models.EmailField(blank=True, null=True)  # Made optional
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='NEW')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asset_id} - {self.make} {self.model}"

    class Meta:
        ordering = ['-registration_date']

    def save(self, *args, **kwargs):
        if not self.asset_id:
            # Get the last asset's ID number
            last_asset = Asset.objects.order_by('-asset_id').first()
            if last_asset and last_asset.asset_id.startswith('BDAsset-'):
                last_number = int(last_asset.asset_id.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1
            # Generate the new asset ID
            self.asset_id = f'BDAsset-{new_number:03d}'
        super().save(*args, **kwargs)

    def get_ram_display(self):
        if self.ram:
            return f"{self.ram} {self.ram_unit}"
        return "-"

    def get_storage_display(self):
        if self.storage:
            return f"{self.storage} {self.storage_unit}"
        return "-"
