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
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source='company'
    )
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Branch
        fields = [
            'id', 'company_id', 'company_name', 'name', 'city', 'country',
            'address', 'phone', 'email', 'branch_head', 'employee_count',
            'dept_count', 'status', 'created_at', 'updated_at'
        ]


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(),
        source='branch',
        allow_null=True,
        required=False
    )
    team_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'branch_id', 'branch_name', 'name', 'head',
            'employee_count', 'team_count', 'status', 'created_at', 'updated_at'
        ]

    def get_team_count(self, obj):
        if not obj.name:
            return 0
        return Team.objects.filter(department__iexact=obj.name).count()





class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    department_id = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'department', 'department_id', 'lead',
            'member_count', 'status', 'description', 'created_at', 'updated_at'
        ]

    def get_department_id(self, obj):
        if not obj.department:
            return None
        # Find the department matching the team's department name
        dept = Department.objects.filter(name__iexact=obj.department).first()
        return dept.id if dept else None



class ShiftDaysField(serializers.Field):
    def to_representation(self, value):
        if not value:
            return []
        return [day.strip() for day in value.split(',') if day.strip()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Days must be a list of strings.")
        return ",".join(str(day) for day in data)


class ShiftSerializer(serializers.ModelSerializer):
    break_minutes = serializers.IntegerField(source='break_duration', required=False, default=0)
    type = serializers.ChoiceField(choices=Shift.SHIFT_TYPE_CHOICES, source='shift_type', default='fixed')
    days = ShiftDaysField(required=False)
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Shift
        fields = [
            'id', 'name', 'start_time', 'end_time', 'days',
            'break_minutes', 'type', 'employee_count', 'status',
            'created_at', 'updated_at'
        ]

    def get_employee_count(self, obj):
        return 0


class CostCenterOwnerField(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.name
        return ""

    def to_internal_value(self, data):
        if not data:
            return None
        
        name_str = str(data).strip()
        from apps.hr.models import Employee
        employee = Employee.objects.filter(name__iexact=name_str).first()
        if not employee:
            import uuid
            emp_id = f"EMP-{uuid.uuid4().hex[:6].upper()}"
            employee = Employee.objects.create(
                emp_id=emp_id,
                name=name_str,
                status='active'
            )
        return employee


class CostCenterSerializer(serializers.ModelSerializer):
    owner = CostCenterOwnerField(required=False, allow_null=True)

    class Meta:
        model = CostCenter
        fields = [
            'id', 'code', 'name', 'type', 'owner', 'budget', 'spent',
            'status', 'created_at', 'updated_at'
        ]


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
