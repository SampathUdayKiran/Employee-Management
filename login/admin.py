from django.contrib import admin

from login.models import EmployeeModel, LeavesHistoryModel, LeavesModel

# Register your models here.
admin.site.register(EmployeeModel)
admin.site.register(LeavesModel)
admin.site.register(LeavesHistoryModel)
