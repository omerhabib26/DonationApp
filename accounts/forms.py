from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

USER_ROLES = (
    ('financer', 'Financer'),
    ('consumer', 'Consumer'),
)


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=255)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=GENDER_TYPES, widget=forms.Select())
    user_roles = forms.ChoiceField(choices=USER_ROLES, widget=forms.Select())
    date_of_birth = forms.DateField(initial='2000-01-01')
    country = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    district = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    area = forms.CharField(max_length=150)
    mobile = forms.CharField(max_length=10, initial='0')
    financer = forms.ModelChoiceField(queryset=User.objects.filter(user_roles='financer'), widget=forms.HiddenInput(),
                                      required=False)
    consumer = forms.ModelChoiceField(queryset=User.objects.filter(user_roles='financer'),
                                      widget=forms.HiddenInput(),
                                      initial=None,
                                      required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'user_roles', 'date_of_birth',
                  'country', 'state', 'district', 'city', 'area', 'mobile')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['financer'].required = False

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
