from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Financer, Consumer
from django.utils import timezone
from .forms import SignUp, LoginForm, FinancerForm, ConsumerForm
from django.contrib import auth
from django.contrib.auth import authenticate


def index(request):
        return render(request, 'accounts/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)

        # if form.is_valid():
        #     return redirect('accounts:index')

        if request.POST['password'] == request.POST['password2']:
            if request.POST['type'] == 'financer':
                try:
                    financer = Financer.objects.get(username=request.POST['username'])
                    return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
                except Financer.DoesNotExist:
                    try:
                        financer = Financer.objects.get(email=request.POST['email'])
                        return render(request, 'accounts/signup.html',
                                      {'error': 'Email is already associated with another account'})
                    except Financer.DoesNotExist:
                        financer = FinancerForm(request.POST, files=request.FILES)

                        if financer.is_valid():
                            user = financer.save(commit=False)
                            user.set_password(request.POST['password'])
                            user.save()
                            return redirect('accounts:index')
                        else:
                            return render(request, 'accounts/signup.html', {'form': form})

            elif request.POST['type'] == 'consumer':
                try:
                    consumer = Consumer.objects.get(username=request.POST['username'])
                    return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
                except Consumer.DoesNotExist:
                    try:
                        consumer = Consumer.objects.get(email=request.POST['email'])
                        return render(request, 'accounts/signup.html',
                                      {'error': 'Email is already associated with another account'})
                    except Consumer.DoesNotExist:
                        consumer = ConsumerForm(request.POST, files=request.FILES)

                        if consumer.is_valid():
                            consumer.save()
                            return redirect('accounts:index')
                        else:
                            return render(request, 'accounts/signup.html', {'form': form})
        else:
            return render(request, 'accounts/signup.html', {'error': 'Password does not matched'})
    else:
        return render(request, 'accounts/signup.html', )


def login(request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            # #
            # user = Financer.objects.get(email=form.cleaned_data.get('email'))
            # user.check_password(form.cleaned_data['password'])
            # user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(email=email, password=password)

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
