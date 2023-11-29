from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EmployeeModel(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    employee_name = models.CharField(max_length=255)
    employee_role = models.CharField(max_length=255, null=True)
    employee_position = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(default=timezone.now)
    employee_phone = models.CharField(max_length=255, null=True)
    email = models.EmailField()
    gender = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)
    employee_date_of_join = models.DateField(default=timezone.now)
    martial_status = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class FileUpload(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/')
    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)


class LeavesModel(models.Model):
    total_annual_leaves = models.IntegerField()
    leaves_consumed = models.IntegerField()
    total_sick_leaves = models.IntegerField()
    sick_leaves_consumed = models.IntegerField()
    total_casual_leaves = models.IntegerField(default=24)
    casual_leaves_consumed = models.IntegerField(default=0)
    unpaid_leaves_consumed = models.IntegerField(default=0)
    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)

class LeavesHistoryModel(models.Model):
    from_date = models.DateField(default=timezone.now)
    to_date = models.DateField(default=timezone.now)
    number_of_days = models.IntegerField()
    approved_by = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    leave_type = models.CharField(max_length=255)
    reason = models.TextField()
    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)
    notify = models.ForeignKey(
        EmployeeModel, on_delete=models.CASCADE, related_name='leave_notifications', default=1)
    
class AttendenceLogModel(models.Model):
    check_in_date=models.DateField()
    check_in_time=models.DateTimeField()
    check_out_time=models.DateTimeField()
    effective_hours=models.DurationField()
    gross_hours=models.DurationField()
    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE)

class HolidayCalenderModel(models.Model):
    name=models.CharField(max_length=255)
    date=models.DateField()
    is_floater=models.BooleanField(default=False)