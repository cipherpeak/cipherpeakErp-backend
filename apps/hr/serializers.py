from rest_framework import serializers
from .models import Employee, AttendanceRecord, LeaveRequest, EmpDocument, EmpDocumentFile


class EmployeeSerializer(serializers.ModelSerializer):
    # Optional so that editing an employee does not force re-sending a password.
    # Creation still supplies one from the "Add Employee" modal.
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    department_name = serializers.CharField(source='department.name', read_only=True, default=None)
    branch_name = serializers.CharField(source='branch.name', read_only=True, default=None)

    class Meta:
        model = Employee
        fields = [
            'id', 'emp_id', 'name', 'email', 'phone', 'avatar_initials', 'avatar_color',
            'department', 'department_name', 'branch', 'branch_name', 'designation',
            'shift', 'manager', 'join_date', 'nationality', 'gender', 'status',
            'is_active', 'is_staff', 'created_at', 'updated_at', 'password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        employee = Employee(**validated_data)
        if password:
            employee.set_password(password)
        else:
            employee.set_unusable_password()
        employee.save()
        return employee

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class EmployeeListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True, default=None)
    branch_name = serializers.CharField(source='branch.name', read_only=True, default=None)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['password']


class AttendanceRecordSerializer(serializers.ModelSerializer):
    emp_name = serializers.CharField(source='employee.name', read_only=True, default=None)
    avatar_initials = serializers.CharField(source='employee.avatar_initials', read_only=True, default=None)
    avatar_color = serializers.CharField(source='employee.avatar_color', read_only=True, default=None)
    department = serializers.CharField(source='employee.department.name', read_only=True, default=None)

    class Meta:
        model = AttendanceRecord
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    emp_name = serializers.CharField(source='employee.name', read_only=True, default=None)
    avatar_initials = serializers.CharField(source='employee.avatar_initials', read_only=True, default=None)
    avatar_color = serializers.CharField(source='employee.avatar_color', read_only=True, default=None)
    department = serializers.CharField(source='employee.department.name', read_only=True, default=None)

    class Meta:
        model = LeaveRequest
        fields = '__all__'


class EmpDocumentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpDocumentFile
        fields = ['id', 'file', 'file_name', 'uploaded_at']


class EmpDocumentSerializer(serializers.ModelSerializer):
    emp_name = serializers.CharField(source='employee.name', read_only=True, default=None)
    avatar_initials = serializers.CharField(source='employee.avatar_initials', read_only=True, default=None)
    avatar_color = serializers.CharField(source='employee.avatar_color', read_only=True, default=None)
    files = EmpDocumentFileSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = EmpDocument
        fields = [
            'id', 'employee', 'emp_name', 'avatar_initials', 'avatar_color', 'type',
            'document_number', 'issue_date', 'expiry_date', 'status',
            'created_at', 'updated_at', 'files', 'uploaded_files',
        ]
