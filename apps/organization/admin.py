from django.contrib import admin
from .models import Company, Branch, Plant, Department, Designation, Team, Shift


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'legal_name', 'initials', 'industry', 'country', 'status', 'created_at')
    search_fields = ('name', 'legal_name')
    list_filter = ('status', 'industry', 'country')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'city', 'country', 'employee_count', 'status', 'created_at')
    search_fields = ('name', 'company__name')
    list_filter = ('status', 'country')


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'branch_name', 'type', 'status', 'created_at')
    search_fields = ('name', 'branch_name')
    list_filter = ('status', 'type')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'branch', 'branch_name', 'employee_count', 'status', 'created_at')
    search_fields = ('name', 'branch_name')
    list_filter = ('status',)


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'level', 'grade', 'min_salary', 'max_salary', 'status', 'created_at')
    search_fields = ('title', 'department')
    list_filter = ('status', 'level')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'lead', 'member_count', 'status', 'created_at')
    search_fields = ('name', 'department')
    list_filter = ('status',)


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'days', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('status',)
