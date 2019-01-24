from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from  django.utils.translation import ugettext_lazy as _


GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_superuser, is_admin, **extra_fields):

        now = datetime.now()

        user = self.model(username=username,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.is_admin = is_admin
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False, False, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        return self._create_user(username, password, True, True, True, **extra_fields)


class Financer(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_TYPES, max_length=10)
    password = models.CharField(max_length=31)
    profile_pic = models.ImageField(upload_to='images/', null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, primary_key=True, unique=True)
    date_of_birth = models.DateField(default='2000-01-01')
    mobile = models.CharField(max_length=11, default=0)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    account_balance = models.BigIntegerField(default=0)

    date_joined = models.DateTimeField(_('date joined'), default=datetime.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    # this methods are require to login super user from admin panel
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_admin


class Consumer(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_TYPES, max_length=10)
    password = models.CharField(max_length=31)
    occupation = models.CharField(max_length=255, null=True)
    profile_pic = models.ImageField(upload_to='images/', null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(default='2000-01-01')
    mobile = models.CharField(max_length=11, default=0)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    financer = models.ForeignKey(Financer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


