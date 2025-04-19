import re
from datetime import time
from django.db import models
from django.db import transaction
from django.dispatch import receiver
from gdstorage.storage import GoogleDriveStorage
from django.db.models.signals import m2m_changed

        
gd_storage = GoogleDriveStorage()

class Counter(models.Model):
    collection_name = models.CharField(max_length=100, unique=True)
    current_id = models.IntegerField(default=0)

    class Meta:
        db_table = 'counters'

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
    
class AnnouncementImage(models.Model):
    title = models.CharField(max_length=200, blank=False, help_text="Image title")
    image = models.ImageField(upload_to='sejong/announcements', storage=gd_storage, help_text="Image file")
    google_drive_file_id = models.CharField(max_length = 100, blank = True, null = True, help_text = "Google Drive file Id")


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        file_url = self.image.storage.url(self.image.name)  # Print the URL of the uploaded image

        # Extract the file ID from the URL
        match = re.search(r'id=([^&]+)', file_url)

        self.google_drive_file_id = f'https://drive.google.com/thumbnail?id={match.group(1)}' if match else None
        super().save(update_fields = ['google_drive_file_id'])

class Announcement(models.Model):
    """
    Model for storing announcements (Django relational model)
    """
    custom_id = models.IntegerField(unique = True, blank = True, null = True)
    title = models.CharField(max_length=200, blank=False, help_text="Announcement title")
    content = models.TextField(blank=False, help_text="Announcement content")
    images_many_to_many = models.ManyToManyField(AnnouncementImage, blank=True, help_text="Images related to the announcement")
    images = models.JSONField(blank=True, null=True, help_text="Serialized images")
    time_posted = models.DateTimeField(auto_now_add=True, help_text="Date of announcement")
    author = models.CharField(max_length=100, blank=False, help_text="Author of the announcement")
    is_active = models.BooleanField(default=True, help_text="Is the announcement active?")

    class Meta:
        db_table = 'announcements'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.custom_id is None:
            self.custom_id = get_next_id('announcements')
        
        super().save(*args, **kwargs)

@receiver(m2m_changed, sender=Schedule.time_many_to_many.through)
def update_schedule_time(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.time = []
        for time_slot in instance.time_many_to_many.all():
            instance.time.append({
                "day": time_slot.day,
                "start_time": time_slot.start_time.strftime("%H:%M"),
                "end_time": time_slot.end_time.strftime("%H:%M"),
                "classroom": time_slot.classroom
            })
        instance.save(update_fields=['time'])

@receiver(m2m_changed, sender=Announcement.images_many_to_many.through)
def update_announcement_images(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.images = [img.google_drive_file_id for img in instance.images_many_to_many.all()]
        instance.save(update_fields=['images'])

@transaction.atomic
def get_next_id(collection_name):
    counter, _ = Counter.objects.get_or_create(collection_name=collection_name)
    counter.current_id += 1
    counter.save()
    return counter.current_id
