from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Facility(models.Model):
    FACILITY_TYPES = (
        ('court', 'Court'),
        ('gym', 'Gym'),
        ('pool', 'Pool'),
        ('field', 'Field'),
        ('stadium', 'Stadium'),
    )

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
        ('closed', 'Closed'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Facilities"

class Equipment(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
        ('in_use', 'In Use'),
    )

    EQUIPMENT_TYPES = (
        ('fixed', 'Fixed Equipment'),
        ('movable', 'Movable Equipment'),
        ('electronic', 'Electronic Equipment'),
        ('sports', 'Sports Equipment'),
    )

    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    purchase_date = models.DateField(null=True, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.facility.name})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    purpose = models.CharField(max_length=200)
    participants = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.facility.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-start_time']
        # Add constraint to prevent double bookings
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name='valid_booking_time_range'
            ),
        ]

class MaintenanceRecord(models.Model):
    STATUS_CHOICES = (
        ('reported', 'Reported'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='maintenance_records', null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_records', null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    def __str__(self):
        if self.facility:
            return f"Issue with {self.facility.name}"
        elif self.equipment:
            return f"Issue with {self.equipment.name}"
        else:
            return f"Maintenance record #{self.id}"

class UsageLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='usage_logs')
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_logs')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Usage log for {self.booking}"

# Create a profile model to extend the User model
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"