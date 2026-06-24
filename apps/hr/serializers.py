from rest_framework import serializers
from .models import Employee, AttendanceRecord, LeaveRequest, EmpDocument


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'


class EmpDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpDocument
        fields = '__all__'
