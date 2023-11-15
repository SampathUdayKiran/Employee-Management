from django.urls import path
from .views import EmployeeModelList, FileUploadView, UserRegistrationView, UserLoginView,UserListView, YourApiView, download_file

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('employees/', EmployeeModelList.as_view(), name='employee-list'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('download/<int:file_id>/', download_file, name='download-file'),
    path('async', YourApiView.as_view(), name='async'),
]