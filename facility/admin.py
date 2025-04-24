from django.contrib import admin
from .models import Facility, Equipment, Booking, MaintenanceRecord, UsageLog, UserProfile

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'location', 'status', 'created_at')
    list_filter = ('type', 'status')
    search_fields = ('name', 'location')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility', 'type', 'status', 'purchase_date')
    list_filter = ('type', 'status', 'facility')
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('facility', 'user', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'facility')
    search_fields = ('user__username', 'facility__name')
    date_hierarchy = 'start_time'

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('get_issue_name', 'reported_by', 'status', 'reported_at')
    list_filter = ('status',)
    search_fields = ('issue_description', 'reported_by__username')
    date_hierarchy = 'reported_at'

    def get_issue_name(self, obj):
        if obj.facility:
            return f"Issue with {obj.facility.name}"
        elif obj.equipment:
            return f"Issue with {obj.equipment.name}"
        else:
            return f"Maintenance record #{obj.id}"

    get_issue_name.short_description = 'Issue'

@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    list_display = ('booking', 'check_in_time', 'check_out_time', 'staff')
    list_filter = ('booking__facility',)
    search_fields = ('booking__user__username', 'booking__facility__name')
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')