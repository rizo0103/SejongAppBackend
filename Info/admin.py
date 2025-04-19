from django.contrib import admin
from .models import Schedule, TimeSlot, Announcement, AnnouncementImage

# Register Schedule model
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    pass

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'classroom')  # Customize fields to display in admin
    search_fields = ('day', 'start_time', 'end_time', 'classroom')      # Add search functionality
    list_filter = ('day', 'start_time', 'end_time', 'classroom')        # Add filter options

@admin.register(AnnouncementImage)
class AnnouncementImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
    search_fields = ('image',)  # Add search functionality
    list_filter = ('image',)