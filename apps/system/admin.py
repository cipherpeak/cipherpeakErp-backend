from django.contrib import admin
from .models import Role, SystemUser, ApprovalWorkflow, Delegation, LoginEvent, DeviceSession


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count', 'is_system', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_system',)


@admin.register(SystemUser)
class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'role', 'branch', 'department', 'status', 'two_fa', 'last_login')
    search_fields = ('name', 'email')
    list_filter = ('status', 'two_fa', 'role')
    readonly_fields = ('last_login', 'created_at', 'updated_at')


@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = ('module', 'step_order', 'approver_role', 'threshold', 'auto_approve_under', 'status', 'current_pending')
    search_fields = ('module',)
    list_filter = ('status',)


@admin.register(Delegation)
class DelegationAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'start_date', 'end_date', 'status')
    search_fields = ('from_user__name', 'to_user__name')
    list_filter = ('status',)


@admin.register(LoginEvent)
class LoginEventAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'timestamp', 'ip', 'device', 'location', 'status', 'method')
    search_fields = ('user_name',)
    list_filter = ('status', 'method')
    readonly_fields = ('timestamp',)


@admin.register(DeviceSession)
class DeviceSessionAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'device', 'browser', 'ip', 'location', 'last_active', 'status')
    search_fields = ('user_name',)
    list_filter = ('status',)
    readonly_fields = ('last_active',)
