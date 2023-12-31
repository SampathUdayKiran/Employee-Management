from django.utils import timezone
import os
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from alfazance import settings
from login.models import EmployeeModel
from login.serializers import EmployeeModelSerializer, UserLoginSerializer, UserSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from .models import AttendenceLogModel, FileUpload, HolidayCalenderModel, LeavesHistoryModel, LeavesModel
from .serializers import ApplyLeavesSerializer, AttendenceLogSerializer, CheckInSerializer, CheckOutSerializer, EmployeeLeaveApproveSerializer, FileUploadSerializer, HolidayCalenderSerializer, LeavesHistorySerializer, LeavesModelSerializer
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import subprocess
from rest_framework import viewsets
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlencode
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.data['username'], password=serializer.data['password'], email=serializer.data['email'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

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


class EmployeePositionAPIView(generics.ListAPIView):
    serializer_class = EmployeeModelSerializer

    def get_queryset(self):
        position = self.kwargs['employee_position']
        return EmployeeModel.objects.filter(employee_position=position)


class FileUploadView(CreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        employee_id = request.data.get('employee')
        print(request.data)
        print(employee_id)
        try:
            file_upload_instance = FileUpload.objects.filter(
                employee=employee_id).order_by('-id').first()
            print(file_upload_instance)
            if file_upload_instance:
                existing_file_path = os.path.join(
                    settings.MEDIA_ROOT, str(file_upload_instance.file))
                if os.path.exists(existing_file_path):
                    os.remove(existing_file_path)
                serializer = self.get_serializer(
                    file_upload_instance, data=request.data, partial=True)
            else:
                serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)


class EmployeeCreateAPIView(generics.CreateAPIView):
    serializer_class = EmployeeModelSerializer

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
        return LeavesHistoryModel.objects.filter(employee_id=employee_id).order_by('-id')


class ApplyLeaveAPIView(generics.CreateAPIView):
    serializer_class = ApplyLeavesSerializer

    def post(self, request, *args, **kwargs):
        serializer = ApplyLeavesSerializer(data=request.data)
        if serializer.is_valid():
            employee_id = serializer.validated_data['employee']
            leaves_model = LeavesModel.objects.get(employee_id=employee_id)
            if (serializer.validated_data['leave_type'] == 'sick'):
                if (leaves_model.total_sick_leaves-leaves_model.sick_leaves_consumed >= serializer.validated_data['number_of_days']):
                    # leaves_model.total_sick_leaves -= serializer.validated_data['number_of_days']
                    # leaves_model.total_annual_leaves -= serializer.validated_data['number_of_days']
                    leaves_model.sick_leaves_consumed += serializer.validated_data['number_of_days']
                    leaves_model.leaves_consumed += serializer.validated_data['number_of_days']
                else:
                    return Response({'message': 'Exceeded maximum sick leave limit'}, status=status.HTTP_400_BAD_REQUEST)
            elif (serializer.validated_data['leave_type'] == 'casual'):
                if (leaves_model.total_casual_leaves-leaves_model.casual_leaves_consumed >= serializer.validated_data['number_of_days']):
                    # leaves_model.total_casual_leaves -= serializer.validated_data['number_of_days']
                    # leaves_model.total_annual_leaves -= serializer.validated_data['number_of_days']
                    leaves_model.casual_leaves_consumed += serializer.validated_data['number_of_days']
                    leaves_model.leaves_consumed += serializer.validated_data['number_of_days']
                else:
                    return Response({'message': 'Exceeded maximum casual leave limit'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                leaves_model.unpaid_leaves_consumed += serializer.validated_data['number_of_days']
            leaves_model.save()
            instance = serializer.save()
            send_email(instance)
            return Response({'message': 'Leave applied sucessfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class EmployeeLeaveApproveAPI(generics.CreateAPIView):
#     serializer_class = EmployeeLeaveApproveSerializer
#     def post(self, request, format=None):
#         serializer = EmployeeLeaveApproveSerializer(data=request.data)
#         if serializer.is_valid():
#             leave=LeavesHistoryModel.objects.get(pk=serializer.data['leave_id'])
#             leave.approved_by=leave.notify
#             leave.status='APPROVED'
#             return Response({'message': 'Leave approved'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EmployeeLeaveApproveAPI(APIView):
    def get(self, request, leave_id):
        try:
            leave = LeavesHistoryModel.objects.get(pk=leave_id)
            if (leave.status == 'PENDING'):
                leave.approved_by = leave.notify.employee_name
                leave.status = 'APPROVED'
                leave.save()
                return Response({'message': 'Leave approved'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Action not allowed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


class EmployeeLeaveCancelAPI(APIView):
    def get(self, request, leave_id):
        try:
            leave = LeavesHistoryModel.objects.get(pk=leave_id)
            if (leave.status == 'PENDING'):
                leave.approved_by = leave.notify.employee_name
                leave.status = 'CANCELLED'
                leaves_model = LeavesModel.objects.get(
                    employee_id=leave.employee.employee_id)
                if (leave.leave_type == 'sick'):
                    leaves_model.sick_leaves_consumed -= leave.number_of_days
                    leaves_model.leaves_consumed -= leave.number_of_days
                elif (leave.leave_type == 'casual'):
                    leaves_model.casual_leaves_consumed -= leave.number_of_days
                    leaves_model.leaves_consumed -= leave.number_of_days
                else:
                    leaves_model.unpaid_leaves_consumed -= leave.number_of_days
                leave.save()
                leaves_model.save()
                return Response({'message': 'Leave cancelled'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Action not allowed'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)

def send_email(leave_id):
    leave = LeavesHistoryModel.objects.get(pk=leave_id.id)
    approval_url = f"{settings.PROD_URL_1}employee-leave-approve/{leave_id.id}/"
    cancellation_url = f"h{settings.PROD_URL_1}employee-leave-cancel/{leave_id.id}/"
    # email_body = render_to_string('leave_approval_email.html', {'leave': leave, 'approval_url': approval_url, 'cancellation_url': cancellation_url})
    email_body = f"""
    <html>
    <body>
        <p>Leave Request Approval:</p>
        <p>Details:</p>
        <ul>
            <li>Employee: {leave.employee.employee_name} ({leave.employee.employee_id})</li>
            <li>From: {leave.from_date}</li>
            <li>To: {leave.to_date}</li>
            <li>Number of Days: {leave.number_of_days}</li>
            <li>Reason: {leave.reason}</li>
        </ul>
        <a href="{approval_url}">Approve</a>
        <a href="{cancellation_url}">Cancel</a>
    </body>
    </html>
    """
    try:
        send_mail(
            'Leave Request Action Required',
            strip_tags(email_body),
            'udaykiranreddy9908@gmail.com',
            [leave.notify.email],
            html_message=email_body,
        )
    except Exception as e:
        print(e)

class AttendenceLogAPIView(generics.CreateAPIView):
    serializer_class=AttendenceLogSerializer

class HolidaysListCreateAPIView(generics.CreateAPIView):
    serializer_class=HolidayCalenderSerializer

# class HolidaysListAPIView(APIView):
#     def get(self, request):
#         holiday_list=HolidayCalenderModel.objects.all()
#         serializer=HolidayCalenderSerializer(data=holiday_list)
#         if(serializer.is_valid()):
#             return serializer.data
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
class HolidaysListAPIView(generics.ListAPIView):
    serializer_class = HolidayCalenderSerializer
    def get_queryset(self):
        # Customize the queryset based on your requirements
        # For example, you can add extra filters, annotations, or any other modifications
        # Filter holidays that are upcoming and set is_floater to True
        try:
            current_date = timezone.now().date()
            next_holiday = HolidayCalenderModel.objects.filter(date__gte=current_date).first()
            queryset =HolidayCalenderModel.objects.all().order_by('date')
            for holiday in queryset:
                if(holiday.id==next_holiday.id):
                    holiday.is_floater=True
            return queryset
        except Exception as e:
            print(e)
class CheckInAPIView(generics.CreateAPIView):
    serializer_class=CheckInSerializer
    def post(self,request):
        try:

            serializer=CheckInSerializer(data=request.data)
            if(serializer.is_valid()):
                current_date = timezone.now().date()
                # log_record=AttendenceLogModel.objects.filter(date=current_date, employee=serializer.data['employee']).first()
                serializer.validated_data['check_in_date']=current_date
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(e)
    
class AttendenceLogListAPIView(generics.ListAPIView):
    serializer_class=AttendenceLogSerializer
    def get_queryset(self):
        try:
            queryset =AttendenceLogModel.objects.all()
            return queryset
        except Exception as e:
            print(e)
            










# class CheckInAPIView(generics.CreateAPIView):
#     serializer_class=CheckOutSerializer

