from .models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LoginForm
from django.contrib import auth
from django.contrib.auth import authenticate


def index(request):
        return render(request, 'accounts/index.html')


def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        try:
            user = User.objects.get(username=form.cleaned_data.get('username'))
            return render(request, 'accounts/signup.html', {'form': form})
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=form.cleaned_data.get('email'))
                return render(request, 'accounts/signup.html',
                              {'form': form})
            except User.DoesNotExist:
                new_user = form.save(commit=False)
                new_user.save()
                new_user = authenticate(username=form.cleaned_data.get('username'),
                                        password=form.cleaned_data.get('password1'))
                auth.login(request, new_user)
                if new_user.is_authenticated:
                    return redirect('accounts:index', )
                else:
                    return HttpResponse('Login Failed')
    else:
        return render(request, 'accounts/signup.html', {'form': form})


def login(request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            # #
            # user = Financer.objects.get(email=form.cleaned_data.get('email'))
            # user.check_password(form.cleaned_data['password'])
            # user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                if user.is_authenticated:
                    return redirect('accounts:index',)
                else:
                    return HttpResponse('Login Failed')
            else:
                return render(request, 'accounts/login.html', {'form': form})
        else:
            return render(request, 'accounts/login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('accounts:index')
