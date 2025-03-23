from django.contrib import admin
from .models import StudentGroup, Announcement, Schedule


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Показываем название группы в списке
    filter_horizontal = ("students",)  # Удобный виджет для выбора студентов



@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "is_active") 
    search_fields = ("title", "message")  
    list_filter = ("created_at", "is_active")  


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('group', 'day_of_week')

