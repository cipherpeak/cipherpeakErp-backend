from django.contrib import admin
from .models import Employee, AttendanceRecord, LeaveRequest, EmpDocument


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'email', 'department', 'designation', 'branch', 'status', 'is_staff', 'join_date')
    search_fields = ('emp_id', 'name', 'email')
    list_filter = ('status', 'department', 'branch', 'is_staff')
    readonly_fields = ('last_login', 'created_at', 'updated_at')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status', 'hours_worked', 'overtime_hours')
    search_fields = ('employee__name', 'employee__emp_id')
    list_filter = ('status', 'date')
    readonly_fields = ('created_at',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'type', 'start_date', 'end_date', 'days', 'status', 'approved_by', 'created_at')
    search_fields = ('employee__name', 'employee__emp_id')
    list_filter = ('status', 'type')
    readonly_fields = ('created_at',)


@admin.register(EmpDocument)
class EmpDocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'type', 'document_number', 'issue_date', 'expiry_date', 'status', 'created_at')
    search_fields = ('employee__name', 'document_number')
    list_filter = ('status', 'type')
    readonly_fields = ('created_at', 'updated_at')
