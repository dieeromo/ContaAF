from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from afnet.decorators import custom_permission_required

# Create your views here.

def home(request):

    return render(request, 'home.html',{
    })

def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form':UserCreationForm,
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #reguster user
            try:
                user= User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                print('usuario registrado')
                login(request, user)
                return redirect('task')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form':UserCreationForm,
                    'error':'El usuario ya existe'
                })
        return render(request, 'signup.html',{
            'form':UserCreationForm,
            'error':'Las contraseñas no coinciden'
        })

@login_required
def task(request):
    return render(request, 'task.html')


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form':AuthenticationForm,
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form':AuthenticationForm,
                'error':'Usuario o contraseña invalido'
            })
        else:
            login(request, user)
            return redirect('task')


@custom_permission_required(allowed_roles=['manager'])
def pagesocios(request):
    
    return render(request, 'pagesocios.html')