from rest_framework import serializers
from django.contrib.auth.models import User
from login.models import EmployeeModel
from .models import FileUpload, LeavesHistoryModel, LeavesModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        # extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class EmployeeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'


class LeavesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavesModel
        fields = '__all__'


class LeavesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavesHistoryModel
        fields = '__all__'

    def validate(self, data):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        if from_date and to_date:
            # Calculate the number of days and add it to the data dictionary
            number_of_days = (to_date - from_date).days + 1
            data['number_of_days'] = number_of_days

        return data
