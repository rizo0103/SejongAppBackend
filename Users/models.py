from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from gdstorage.storage import GoogleDriveStorage
from pymongo import MongoClient
from bson import ObjectId
# Create your models here.
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
    avatar = models.ImageField(upload_to="sejong/users/avatar", blank=True) #storage=gd_storage,
    date_joined = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
