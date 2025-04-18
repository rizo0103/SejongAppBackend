from datetime import time
from django.db import models
from django_mongodb_backend.models import EmbeddedModel
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField

class TimeSlot(models.Model):
    """
    Model that represents time slot in schedule (Django relational model)
    """
    day = models.IntegerField(choices=[
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.IntegerField(choices=[
        (301, 301), 
        (303, 303), 
        (306, 306), 
        (307, 307), 
        (308, 308)
    ])

    def __str__(self):
        return f"{self.get_day_display()} {self.start_time} - {self.end_time} ({self.get_classroom_display()})"


class Schedule(models.Model):
    """
    Model for storing schedule information (Django relational model)
    """
    group = models.CharField(max_length=50, blank=False, help_text="Group name")

    time_many_to_many = models.ManyToManyField(
        TimeSlot,
        blank=False,
        help_text="Time slots for the schedule"
    )
    time = models.JSONField(blank=True, null=True, help_text="Serialized time slots")

    teacher = models.CharField(max_length=100, blank=False, help_text="Teacher name")
    book = models.IntegerField(
        blank=False,
        choices=[(i, str(i)) for i in range(1, 9)],
        help_text="Book number (from 1 to 8)"
    )

    class Meta:
        db_table = 'schedules'

    def __str__(self):
        return f"{self.group} - {self.teacher}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.time = []

        for time_slot in self.time_many_to_many.all():
            self.time.append({
                "day": time_slot.day,
                "start_time": time_slot.start_time.strftime("%H:%M"),
                "end_time": time_slot.end_time.strftime("%H:%M"),
                "classroom": time_slot.classroom
            })

        super().save(*args, **kwargs)
