from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class EmployeeModel(models.Model):
    employeeId = models.IntegerField(primary_key=True)
    employeeName = models.CharField(max_length=255)
    employeeRole = models.CharField(max_length=255,null=True)
    dateOfBirth = models.DateField(default=timezone.now)
    employeePhone = models.CharField(max_length=255,null=True)
    email = models.EmailField()
    gender = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)
    employeeDateOfJoin = models.DateField(default=timezone.now)
    martialStatus = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class FileUpload(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')

class LeavesModel(models.Model):
    total_annual_leaves=models.IntegerField()
    leaves_consumed=models.IntegerField()
    total_sick_leaves=models.IntegerField()
    sick_leaves_consumed=models.IntegerField()
    employee_id=models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)

class LeavesHistoryModel(models.Model):
    from_date=models.DateField(default=timezone.now)
    to_date=models.DateField(default=timezone.now)
    number_of_days=models.IntegerField()
    approved_by=models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    leave_type=models.CharField(max_length=255)
    reason=models.TextField()
    employee_id=models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)
    

