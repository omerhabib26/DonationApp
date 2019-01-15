from django.db import models


GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class Financer(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_TYPES, max_length=10)
    profile_pic = models.ImageField(upload_to='images/')
    username = models.EmailField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(default='2000-01-01')
    mobile = models.CharField(max_length=11, default=0)
    address = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    account_balance = models.BigIntegerField()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


class Consumer(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_TYPES, max_length=10)
    occupation = models.CharField(max_length=255, null=True)
    profile_pic = models.ImageField(upload_to='images/', null=True)
    username = models.EmailField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(default='2000-01-01')
    mobile = models.CharField(max_length=11, default=0)
    address = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    financer = models.ForeignKey(Financer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


