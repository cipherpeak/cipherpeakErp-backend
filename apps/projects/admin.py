from django.contrib import admin
from .models import (
    Project, Milestone, ProjectTask, Site, SiteVisitor, SiteIncident, SiteProgress,
    Resource, ResourceAllocation, Timesheet, TimesheetEntry,
    ProjectBilling, ProjectBillingInvoice, ProjectCosting, ProjectCostComponent,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'customer_name', 'manager', 'start_date', 'end_date', 'budget', 'actual_cost', 'completion_pct', 'status', 'priority', 'created_at')
    search_fields = ('code', 'name', 'customer_name', 'manager')
    list_filter = ('status', 'priority', 'billing_type')


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('milestone_number', 'project', 'name', 'due_date', 'completed_date', 'owner', 'completion_pct', 'status', 'payment_linked', 'created_at')
    search_fields = ('milestone_number', 'name')
    list_filter = ('status', 'payment_linked')


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('task_number', 'project', 'milestone', 'title', 'status', 'priority', 'assignee', 'start_date', 'due_date', 'estimated_hours', 'logged_hours', 'billable')
    search_fields = ('task_number', 'title', 'assignee')
    list_filter = ('status', 'priority', 'billable')


class SiteVisitorInline(admin.TabularInline):
    model = SiteVisitor
    extra = 0


class SiteIncidentInline(admin.TabularInline):
    model = SiteIncident
    extra = 0


class SiteProgressInline(admin.TabularInline):
    model = SiteProgress
    extra = 0


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('site_code', 'name', 'project', 'location', 'site_manager', 'status', 'start_date', 'end_date', 'overall_progress', 'created_at')
    search_fields = ('site_code', 'name', 'location')
    list_filter = ('status',)
    inlines = [SiteVisitorInline, SiteIncidentInline, SiteProgressInline]


class ResourceAllocationInline(admin.TabularInline):
    model = ResourceAllocation
    extra = 0


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resource_number', 'name', 'type', 'category', 'department', 'daily_cost', 'hourly_cost', 'utilization_pct', 'availability', 'created_at')
    search_fields = ('resource_number', 'name')
    list_filter = ('type', 'availability')
    inlines = [ResourceAllocationInline]


class TimesheetEntryInline(admin.TabularInline):
    model = TimesheetEntry
    extra = 0


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('timesheet_number', 'employee', 'week_start', 'week_end', 'status', 'total_hours', 'billable_hours', 'overtime_hours', 'created_at')
    search_fields = ('timesheet_number',)
    list_filter = ('status',)
    inlines = [TimesheetEntryInline]


class ProjectBillingInvoiceInline(admin.TabularInline):
    model = ProjectBillingInvoice
    extra = 0


@admin.register(ProjectBilling)
class ProjectBillingAdmin(admin.ModelAdmin):
    list_display = ('billing_number', 'project', 'billing_type', 'contract_value', 'billed_amount', 'collected_amount', 'balance_due', 'status', 'next_billing_date', 'created_at')
    search_fields = ('billing_number',)
    list_filter = ('status', 'billing_type')
    inlines = [ProjectBillingInvoiceInline]


class ProjectCostComponentInline(admin.TabularInline):
    model = ProjectCostComponent
    extra = 0


@admin.register(ProjectCosting)
class ProjectCostingAdmin(admin.ModelAdmin):
    list_display = ('project', 'budget', 'actual_cost', 'committed_cost', 'forecasted_cost', 'variance', 'variance_pct', 'profitability_pct', 'contract_value', 'updated_at')
    search_fields = ('project__code',)
    inlines = [ProjectCostComponentInline]
