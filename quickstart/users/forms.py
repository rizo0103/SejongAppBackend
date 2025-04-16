from django import forms 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Password",
        help_text="You can change the password using <a href=\"../password/\">this form</a>.")
    

    class Meta:
        model = User
        fields = ('username', 'fullname', 'email', 'phone_number', 'status', 'group', 'avatar', 
                  'is_active', 'is_staff', 'is_superuser')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone.startswith('+992') or len(phone) != 13:
            raise forms.ValidationError("Phone number must be in format +992XXXXXXXXX")
        return phone