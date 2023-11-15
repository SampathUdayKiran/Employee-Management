from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EmployeeModel(models.Model):
    employeeId=models.IntegerField(primary_key=True)
    employeeName=models.CharField(max_length=255)
    email=models.EmailField()
    gender=models.CharField(max_length=255)
    dateOfBirth=models.DateField()
    martialStatus=models.CharField(max_length=255)
    nationality=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class FileUpload(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')

