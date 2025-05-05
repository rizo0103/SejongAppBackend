from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from gdstorage.storage import GoogleDriveStorage
import re
from django.utils.html import format_html
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

gd_storage = GoogleDriveStorage()

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        email = extra_fields.get('email')
        if email:
            extra_fields['email'] = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
            return self.get(username=username)



class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    
    phone_validator = RegexValidator(
    regex=r'^\+992\d{9}$',
    message="Phone number must start with '+992' and be followed by exactly 9 digits."
)

    STATUS_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin')
    )
    username = models.CharField(max_length=100, unique=True, blank=False)
    fullname = models.CharField(max_length=200, blank=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13, validators=[phone_validator], blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Student')
    group = models.ManyToManyField("Groups", related_name="user_set", blank=True)  
    avatar = models.ImageField(upload_to="SejongApp/users/avatars", storage=gd_storage, blank=True) 
    date_joined = models.DateTimeField(default=timezone.now)
    avatar_id = models.CharField(max_length=250, blank=True, null=True, help_text="Don't touch!!!")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def get_groups(self):
        return [group.name for group in self.group.all()]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            avatar_url = self.avatar.storage.url(self.avatar.name)
            match_avatar = re.search(r'id=([^&]+)', avatar_url)
            self.avatar_id = f'https://drive.google.com/thumbnail?id={match_avatar.group(1)}' if match_avatar else None
            super().save(update_fields = ['avatar_id'])

    def __str__(self):
        return self.username



class Groups(models.Model):    
    name = models.CharField(max_length=100, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def user_count(self):
        return self.user_set.count()
    
    user_count.short_description = "Count of Participants"

    def participant_names(self):
        return [user.fullname for user in self.user_set.all()]
    
    def participant_names_admin(self):
        return format_html("<br>".join(user.fullname for user in self.user_set.all()))
    
    participant_names_admin.short_description = "Participants"

    class Meta:
        db_table = 'groups'
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)