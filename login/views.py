# from django.shortcuts import render
# from rest_framework.decorators import api_view
import os
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from login.models import EmployeeModel
from login.serializers import EmployeeModelSerializer, UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .models import FileUpload, LeavesHistoryModel, LeavesModel
from .serializers import FileUploadSerializer, LeavesHistorySerializer, LeavesModelSerializer
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import subprocess
from rest_framework import viewsets


# @api_view(['GET', 'POST'])

# def authentication(request):
#     if request.method=='GET':
#         return ()
#     else:
#         return()

# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

# # views.py

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.data['username'], password=serializer.data['password'], email=serializer.data['email'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Bad Request'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=serializer.data['username'], password=serializer.data['password'])

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'message': 'login sucessfull', 'userId': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]


class EmployeeModelList(generics.ListAPIView):
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeModelSerializer
    # permission_classes = [IsAuthenticated]


class FileUploadView(CreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer


class EmployeeCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = EmployeeModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def download_file(request, file_id):
    file = get_object_or_404(FileUpload, id=file_id)
    file_path = file.file.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response


class YourApiView(APIView):
    def get(self, request):
        try:
            subprocess.Popen(
                ['venv\\Scripts\\python', 'manage.py', 'run_background'])
            return Response({'message': 'Task creation successful'})
        except Exception as e:
            return Response({'error': 'API request failed', 'exception': str(e)}, status=500)


class EmployeeDetailsAPIView(APIView):
    def get(self, request, user_id, format=None):
        try:
            employee = EmployeeModel.objects.get(user=user_id)
            serializer = EmployeeModelSerializer(employee)
            return Response(serializer.data)
        except EmployeeModel.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)


class EmployeeLeavesAPIView(APIView):
    def get(self, request, emp_id, format=None):
        try:
            leaves_details = LeavesModel.objects.get(employee_id=emp_id)
            serializer = LeavesModelSerializer(leaves_details)
            return Response(serializer.data)
        except LeavesModel.DoesNotExist:
            return Response({"error": "Leaves Details not found"}, status=status.HTTP_404_NOT_FOUND)


class LeavesHistoryViewSet(viewsets.ModelViewSet):
    queryset = LeavesHistoryModel.objects.all()
    serializer_class = LeavesHistorySerializer
    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return LeavesHistoryModel.objects.filter(employee_id=employee_id)


class ApplyLeaveAPIView(APIView):
    # def post(self, request):
    #     serializer = LeavesHistorySerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, *args, **kwargs):
        serializer = LeavesHistorySerializer(data=request.data)
        if serializer.is_valid():
            employee_id = serializer.validated_data['employee_id']
            leaves_model = LeavesModel.objects.get(employee_id=employee_id)
            # from_date = serializer.validated_data['from_date']
            # to_date = serializer.validated_data['to_date']
            # number_of_days = (to_date - from_date).days + 1
            # serializer.validated_data['number_of_days'] = number_of_days
            serializer.save()
            # leave_details=LeavesModel.objects.get(employee_id=serializer.validated_data['employee_id'])
            # Return a successful response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return an error response if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
