from django.urls import path
from .views import EmployeeModelList, UserRegistrationView, UserLoginView,UserListView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('employees/', EmployeeModelList.as_view(), name='employee-list'),
]