from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
  title= models.CharField(max_length=100)
  description=models.TextField(blank=True)
  created= models.DateTimeField(auto_now_add=True)
  completed= models.BooleanField(default=False)
  datecompleted= models.DateTimeField(blank=True, null=True)
  important= models.BooleanField(default=False)
  user= models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self) -> str:
    return self.title + ' - by: ' + self.user.username