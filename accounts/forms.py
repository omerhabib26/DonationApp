from django import forms
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Financer, Consumer
from django.contrib.auth import authenticate


GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class FinancerForm(ModelForm):
    class Meta:
        model = Financer
        fields = ['first_name', 'last_name', 'gender', 'password', 'profile_pic', 'username', 'email', 'date_of_birth',
                  'mobile', 'address', 'city', 'state', 'country']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

    def save(self, commit=True):
        user = super(FinancerForm, self).save(commit=False)
        user.set_password(user.password)  # set password properly before commit
        if commit:
            user.save()
        return user


class ConsumerForm(ModelForm):
    class Meta:
        model = Consumer
        fields = ['first_name', 'last_name', 'gender', 'password', 'profile_pic', 'username', 'email', 'date_of_birth',
                  'mobile', 'address', 'city', 'state', 'country']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class SignUp(forms.Form):

    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    gender = forms.ChoiceField()
    date_of_birth = forms.DateField()
    mobile = forms.CharField(max_length=11)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

