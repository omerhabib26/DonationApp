from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from accounts.forms import CustomUserCreationForm
from .models import User

GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

USER_ROLES = (
    ('financer', 'Financer'),
    ('consumer', 'Consumer'),
)


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=255)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=GENDER_TYPES, widget=forms.Select())
    user_roles = forms.ChoiceField(choices=USER_ROLES, widget=forms.Select())
    date_of_birth = forms.DateField(initial='2000-01-01')
    is_active = forms.BooleanField(initial=True)
    is_staff = forms.BooleanField(initial=True)
    is_admin = forms.BooleanField(initial=False)
    country = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    district = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    area = forms.CharField(max_length=150)
    mobile = forms.CharField(max_length=10, initial='0')
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'user_roles', 'date_of_birth',
                  'is_active', 'is_staff', 'is_admin', 'country', 'state', 'district', 'city', 'area', 'mobile')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    change_form = UserChangeForm
    creation_form = CustomUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'gender', 'user_roles', 'date_of_birth', 'mobile',)}),
        ('Address', {'fields': ('country', 'state', 'district', 'city', 'area',)}),
        ('Permissions', {'fields': ('financer', 'consumer', 'is_admin', 'is_active', 'is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'gender', 'user_roles', 'date_of_birth',
                       'financer', 'consumer', 'is_active', 'is_staff', 'is_admin', 'country', 'state', 'district',
                       'city', 'area',
                       'mobile', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
