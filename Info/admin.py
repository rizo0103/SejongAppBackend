from django.contrib import admin
from .models import Schedule, TimeSlot

# Register Schedule model
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')  # Customize fields to display in admin
    search_fields = ('start_time', 'end_time')      # Add search functionality
    list_filter = ('start_time', 'end_time')        # Add filter options
