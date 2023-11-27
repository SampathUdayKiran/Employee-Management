from django.urls import include, path
from .views import ApplyLeaveAPIView, EmployeeCreateAPIView, EmployeeDetailsAPIView, EmployeeLeaveApproveAPI, EmployeeLeaveCancelAPI, EmployeeLeavesAPIView, EmployeeModelList, EmployeePositionAPIView, FileUploadView, LeavesHistoryViewSet, UserRegistrationView, UserLoginView, UserListView, YourApiView, download_file
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'leaveshistory/(?P<employee_id>[^/.]+)', LeavesHistoryViewSet, basename='leaveshistory')
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('employees/', EmployeeModelList.as_view(), name='employee-list'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('download/<int:file_id>/', download_file, name='download-file'),
    path('async', YourApiView.as_view(), name='async'),
    path('employee/create/', EmployeeCreateAPIView.as_view(), name='employee-create'),
    path('employee-details/<int:user_id>/', EmployeeDetailsAPIView.as_view(), name='employee-details'),
    path('employee-leaves-details/<int:emp_id>/', EmployeeLeavesAPIView.as_view(), name='employee-leaves-details'),
    path('employee-leave-apply/', ApplyLeaveAPIView.as_view(), name='employee-leave-apply'),
    path('', include(router.urls)),
    path('employees-position/<str:employee_position>/', EmployeePositionAPIView.as_view(), name='employee-position-api'),
    path('employee-leave-approve/<int:leave_id>/', EmployeeLeaveApproveAPI.as_view(), name='employee-leave-approve'),  
    path('employee-leave-cancel/<int:leave_id>/', EmployeeLeaveCancelAPI.as_view(), name='employee-leave-cancel'),
]   
