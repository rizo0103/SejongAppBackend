from django.contrib import admin
from .models import User, Groups
from django.contrib.auth.models import Group
from .forms import UserAdminForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    model = User

    list_display = ("username", "fullname", "email", "phone_number", "status", "date_joined", "is_active") #group couldn't add, because group is ManytoMany
    list_filter = list_filter = ("status", "group", "date_joined", "is_active")
    search_fields = ('username', 'fullname', 'email', 'phone_number')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('fullname', 'email', 'phone_number', 'status', 'group', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fullname', 'email', 'phone_number', 'status', 'group', 'avatar', 'password1', 'password2', 'is_staff', 'is_active'  )}
        ),
    )

    ordering = ('-date_joined',)
    exclude = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)

# @admin.register(User)
# class User(admin.ModelAdmin):
#     list_display = ("username", "fullname", "email", "phone_number", "status", "date_joined", "is_active")
#     search_fields = ["username",]
#     list_filter = ("status", "is_active", "date_joined")


@admin.register(Groups)
class Groups(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'user_count')
    search_fields = ('name',)
