from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
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
  user = request.user
  tasks =  Task.objects.filter(user=user, datecompleted__isnull=True)
  return render(request, 'tasks/tasks.html', {
    'tasks': tasks
  })
def tasksCompleted(request):
  user = request.user
  tasks =  Task.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')
  return render(request, 'tasks/tasks.html', {
    'tasks': tasks
  })
def task(request, id):
  print(request.user)
  if(request.method == 'GET'):
    task = get_object_or_404(Task, pk=id,user=request.user)
    form = TaskForm(instance=task)
    # tasks =  Task.objects.filter(user=user, datecompleted__isnull=True)
    return render(request, 'tasks/task.html', {
      'task': task,
      'form': form
    })
  try:
    task = get_object_or_404(Task, pk=id, user=request.user)
    form = TaskForm(request.POST, instance=task)
    form.save()
    return redirect('tasks')
  except ValueError:
    return render(request, 'tasks/task.html', {
      'task': task,
      'form': form,
      'error': 'Error Updating Task'
    })
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
  if(request.method=='GET'):
    return render(request, 'tasks/create-task.html',{
      'form': TaskForm
    })
  # title = request.POST.get('title')
  # description = request.POST.get('description')
  # important = request.POST.get('important')
  
  try:
    form = TaskForm(request.POST)
    new_task = form.save(commit=False)
    user = request.user
    new_task.user = user
    new_task.save()
    print(new_task)
    return redirect('tasks')
  except ValueError:
    return render(request, 'tasks/create-task.html', {
      'form': TaskForm
    } )
def completeTask(request, id):
  task = get_object_or_404(Task, pk=id, user=request.user)
  if(request.method=='POST'):
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')
def deleteTask(request, id):
  task = get_object_or_404(Task, pk=id, user=request.user)
  if(request.method=='POST'):
    task.delete()
    return redirect('tasks')
    