from djongo import models  # ✅ Правильный импорт
from bson import ObjectId  # MongoDB ObjectId
from django.contrib.auth.models import User
from PIL import Image



# -------------------------------- SttudentGroups
class StudentGroup(models.Model):
    id = models.ObjectIdField(primary_key=True, default=ObjectId)  # Fix the ID type
    name = models.CharField(max_length=100, unique=True)
    students = models.ManyToManyField(User, related_name="student_groups",  blank=True)

    class Meta:
        verbose_name = "Student Group"
        verbose_name_plural = "Student Groups"

    def __str__(self):
        return self.name



#---------------------------------------- Anouncements
class Announcement(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)  # Manually assign IDs
    title = models.CharField(max_length=100, unique=True)
    message = models.TextField()
    image = models.ImageField(upload_to='announcements.images', blank=True)  # Поле для изображения
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(choices=[(0, "No"), (1, "Yes")], default=1, blank=False)

    def __str__(self):
        return f"{self.id} - {self.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width >300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)



# #--------------------------------------- Lesson
# class Lesson(models.Model):
#     name = models.CharField(max_length=255)  # Название предмета или урока
#     teacher = models.CharField(max_length=255)  # Преподаватель

#     def __str__(self):
#         return self.name

#--------------------------------------- Schedule
class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Понедельник', 'Понедельник'),
        ('Вторник', 'Вторник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    ]

    _id = models.ObjectIdField()
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        to_field= "name"  # Явно указываем, что связь идёт по ObjectId
    )
    # lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=50, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.group.name} - {self.day_of_week} ({self.start_time} - {self.end_time})"  
    

