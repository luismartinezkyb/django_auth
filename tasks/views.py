from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
# Create your views here.

def home(request):
  return render(request, 'home.html')
def signup(request):
  if(request.method == 'GET'):
    return render(request, 'auth/signup.html', {
      'form': UserCreationForm,
    })
  password1 = request.POST['password1']
  password2 = request.POST['password2']
  username = request.POST['username']
  
  
  if(password1 != password2):
    return render(request, 'auth/signup.html', {
      'form': UserCreationForm,
      'errors': [
        {
          'message': 'Passsword does not match'
        }
      ]
    })
  
  try:
    user = User.objects.create(username=username, password=password1)
    user.set_password(password1) 
    user.save()
  except IntegrityError:
    return render(request, 'auth/signup.html', {
      'form': UserCreationForm,
      'errors': [
        {
          'message': 'User already Exists'
        }
      ]
    })
  
  # login(request, user)
  return redirect('tasks')

def tasks(request):
  return render(request, 'tasks/tasks.html')
def signout(request):
  logout(request)
  return redirect('home')

def signin(request):
  # login(request, user)
  if(request.method == 'GET'):
    return render(request, 'auth/signin.html', {
      'form': AuthenticationForm,
    })
    
  username = request.POST.get('username')
  password = request.POST.get('password')
  
  print(f"Username: {username}")
  print(f"Password: {password}")
  
  user = authenticate(request, username=username, password=password)
  
  print(f"Authenticated user: {user}")
  if user is None:
        return render(request, 'auth/signin.html', {
            'form': AuthenticationForm(),
            'errors': [{'message': 'User does not exist or password is incorrect'}]
        })
    
  login(request, user)
  return redirect('tasks')

# def login(request, user, password):
  
def createTask(request):
  return render(request, 'tasks/create-task.html',{
    'form': TaskForm
  })