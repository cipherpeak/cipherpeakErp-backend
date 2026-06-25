from rest_framework import serializers
from .models import Company, Branch, Plant, Department, Designation, Team, Shift
from apps.hr.models import Employee


class CompanySerializer(serializers.ModelSerializer):
    branch_count = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_branch_count(self, obj):
        return obj.branches.count()

    def get_employee_count(self, obj):
        return Employee.objects.filter(branch__company=obj).count()


class BranchSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Branch
        fields = '__all__'


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'




class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'
