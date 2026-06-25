from rest_framework import serializers
from .models import Company, Branch, Plant, Department, Designation, Team, Shift, CostCenter
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


class CostCenterSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)

    class Meta:
        model = CostCenter
        fields = '__all__'


# ===========================================================================
# ORG CHART SERIALIZERS
# ===========================================================================

class OrgChartTeamSerializer(serializers.ModelSerializer):
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'lead', 'member_count', 'status', 'children_count']

    def get_children_count(self, obj):
        return 0


class OrgChartDepartmentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'head', 'employee_count', 'status', 'children', 'children_count']

    def get_children(self, obj):
        teams = Team.objects.filter(department=obj.name, status='active')
        return OrgChartTeamSerializer(teams, many=True).data

    def get_children_count(self, obj):
        return Team.objects.filter(department=obj.name, status='active').count()


class OrgChartBranchSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = ['id', 'name', 'city', 'employee_count', 'status', 'children', 'children_count']

    def get_children(self, obj):
        departments = Department.objects.filter(branch=obj, status='active')
        return OrgChartDepartmentSerializer(departments, many=True).data

    def get_children_count(self, obj):
        return Department.objects.filter(branch=obj, status='active').count()


class OrgChartCompanySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'industry', 'employee_count', 'status', 'children', 'children_count']

    def get_children(self, obj):
        branches = Branch.objects.filter(company=obj, status='active')
        return OrgChartBranchSerializer(branches, many=True).data

    def get_children_count(self, obj):
        return Branch.objects.filter(company=obj, status='active').count()

    def get_employee_count(self, obj):
        return Employee.objects.filter(branch__company=obj).count()
