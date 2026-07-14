from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class PriorityLevel(models.TextChoices):
    LOW = 'low', 'Low'
    NORMAL = 'normal', 'Normal'
    HIGH = 'high', 'High'
    URGENT = 'urgent', 'Urgent'


class ProjectStatus(models.TextChoices):
    PLANNING = 'planning', 'Planning'
    ACTIVE = 'active', 'Active'
    ON_HOLD = 'on_hold', 'On Hold'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    DELAYED = 'delayed', 'Delayed'


class ProjectBillingType(models.TextChoices):
    FIXED_PRICE = 'fixed_price', 'Fixed Price'
    MILESTONE_BASED = 'milestone_based', 'Milestone Based'
    TIME_MATERIAL = 'time_material', 'Time & Material'
    RETAINER = 'retainer', 'Retainer'


class ProjTaskStatus(models.TextChoices):
    TODO = 'todo', 'To Do'
    IN_PROGRESS = 'in_progress', 'In Progress'
    REVIEW = 'review', 'Review'
    COMPLETED = 'completed', 'Completed'
    BLOCKED = 'blocked', 'Blocked'


class MilestoneStatus(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    DELAYED = 'delayed', 'Delayed'
    AT_RISK = 'at_risk', 'At Risk'


class SiteStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    COMPLETED = 'completed', 'Completed'
    SUSPENDED = 'suspended', 'Suspended'


class ResourceType(models.TextChoices):
    EMPLOYEE = 'employee', 'Employee'
    CONTRACTOR = 'contractor', 'Contractor'
    EQUIPMENT = 'equipment', 'Equipment'
    VEHICLE = 'vehicle', 'Vehicle'
    MACHINE = 'machine', 'Machine'


class TimesheetStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SUBMITTED = 'submitted', 'Submitted'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'


class BillingStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    INVOICED = 'invoiced', 'Invoiced'
    PARTIALLY_PAID = 'partially_paid', 'Partially Paid'
    PAID = 'paid', 'Paid'
    OVERDUE = 'overdue', 'Overdue'
    DISPUTED = 'disputed', 'Disputed'


# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

class Project(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(
        'sales.Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='projects',
    )
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    manager = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    budget = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    billed_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    completion_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.PLANNING)
    type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    billing_type = models.CharField(max_length=20, choices=ProjectBillingType.choices, blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.NORMAL)
    team = models.JSONField(default=list, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if self.customer and not self.customer_name:
            self.customer_name = self.customer.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Milestone
# ---------------------------------------------------------------------------

class Milestone(models.Model):
    milestone_number = models.CharField(max_length=40, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=200)
    due_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    owner = models.CharField(max_length=150, blank=True, null=True)
    completion_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=MilestoneStatus.choices, default=MilestoneStatus.UPCOMING)
    description = models.TextField(blank=True, null=True)
    payment_linked = models.BooleanField(default=False)
    payment_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    deliverables = models.JSONField(default=list, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'
        ordering = ['due_date']

    def __str__(self):
        return f"{self.milestone_number} - {self.name}"


# ---------------------------------------------------------------------------
# Project Task (self-referencing)
# ---------------------------------------------------------------------------

class ProjectTask(models.Model):
    task_number = models.CharField(max_length=40, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    milestone = models.ForeignKey(
        Milestone, on_delete=models.SET_NULL, blank=True, null=True, related_name='tasks',
    )
    parent_task = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subtasks',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ProjTaskStatus.choices, default=ProjTaskStatus.TODO)
    priority = models.CharField(max_length=20, choices=PriorityLevel.choices, default=PriorityLevel.NORMAL)
    assignee = models.CharField(max_length=150, blank=True, null=True)
    reporter = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    estimated_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    logged_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    billable = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    dependencies = models.JSONField(default=list, blank=True, help_text='List of project_task IDs')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project Task'
        verbose_name_plural = 'Project Tasks'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.task_number} - {self.title}"


# ---------------------------------------------------------------------------
# Site
# ---------------------------------------------------------------------------

class Site(models.Model):
    site_code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, blank=True, null=True, related_name='sites',
    )
    location = models.CharField(max_length=250, blank=True, null=True)
    coordinates = models.CharField(max_length=60, blank=True, null=True)
    site_manager = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=20, choices=SiteStatus.choices, default=SiteStatus.ACTIVE)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    area_sqm = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    overall_progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'
        ordering = ['site_code']

    def __str__(self):
        return f"{self.site_code} - {self.name}"


class SiteVisitor(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='visitors')
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=200, blank=True, null=True)
    purpose = models.CharField(max_length=200, blank=True, null=True)
    visit_date = models.DateField(blank=True, null=True)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Site Visitor'
        verbose_name_plural = 'Site Visitors'

    def __str__(self):
        return f"{self.site.site_code} - {self.name}"


class SiteIncident(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='incidents')
    type = models.CharField(max_length=40, blank=True, null=True, help_text='near_miss/first_aid/LTI/property_damage/environmental')
    description = models.TextField(blank=True, null=True)
    incident_date = models.DateField(blank=True, null=True)
    reported_by = models.CharField(max_length=150, blank=True, null=True)
    severity = models.CharField(max_length=20, blank=True, null=True, help_text='low/medium/high')
    status = models.CharField(max_length=30, default='open')

    class Meta:
        verbose_name = 'Site Incident'
        verbose_name_plural = 'Site Incidents'

    def __str__(self):
        return f"{self.site.site_code} - {self.type}"


class SiteProgress(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='progress')
    progress_date = models.DateField()
    overall_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    civil_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mep_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    finishing_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Site Progress'
        verbose_name_plural = 'Site Progress'
        ordering = ['-progress_date']

    def __str__(self):
        return f"{self.site.site_code} - {self.progress_date}"


# ---------------------------------------------------------------------------
# Resource
# ---------------------------------------------------------------------------

class Resource(models.Model):
    resource_number = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=ResourceType.choices)
    category = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(
        'organization.Department', on_delete=models.SET_NULL, blank=True, null=True, related_name='project_resources',
    )
    skills = models.JSONField(default=list, blank=True)
    daily_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    hourly_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    capacity_hours_per_day = models.DecimalField(max_digits=5, decimal_places=2, default=8)
    utilization_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    availability = models.CharField(max_length=30, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
        ordering = ['resource_number']

    def __str__(self):
        return f"{self.resource_number} - {self.name}"


class ResourceAllocation(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='allocations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resource_allocations')
    role = models.CharField(max_length=120, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    hours_per_day = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Resource Allocation'
        verbose_name_plural = 'Resource Allocations'

    def __str__(self):
        return f"{self.resource.resource_number} - {self.project.code}"


# ---------------------------------------------------------------------------
# Timesheet
# ---------------------------------------------------------------------------

class Timesheet(models.Model):
    timesheet_number = models.CharField(max_length=40, unique=True)
    employee = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='timesheets',
    )
    week_start = models.DateField(blank=True, null=True)
    week_end = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TimesheetStatus.choices, default=TimesheetStatus.DRAFT)
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    billable_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    submitted_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='approved_timesheets',
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Timesheet'
        verbose_name_plural = 'Timesheets'
        ordering = ['-created_at']

    def __str__(self):
        return self.timesheet_number


class TimesheetEntry(models.Model):
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='entries')
    entry_date = models.DateField()
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, blank=True, null=True, related_name='timesheet_entries',
    )
    task = models.ForeignKey(
        ProjectTask, on_delete=models.SET_NULL, blank=True, null=True, related_name='timesheet_entries',
    )
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    billable = models.BooleanField(default=False)
    overtime = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Timesheet Entry'
        verbose_name_plural = 'Timesheet Entries'

    def __str__(self):
        return f"{self.timesheet.timesheet_number} - {self.entry_date}"


# ---------------------------------------------------------------------------
# Project Billing
# ---------------------------------------------------------------------------

class ProjectBilling(models.Model):
    billing_number = models.CharField(max_length=40, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='billings')
    billing_type = models.CharField(max_length=20, choices=ProjectBillingType.choices, blank=True, null=True)
    contract_value = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    billed_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    collected_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    retention_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    retention_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    retention_released = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=BillingStatus.choices, default=BillingStatus.DRAFT)
    next_billing_date = models.DateField(blank=True, null=True)
    next_billing_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project Billing'
        verbose_name_plural = 'Project Billings'
        ordering = ['-created_at']

    def __str__(self):
        return self.billing_number


class ProjectBillingInvoice(models.Model):
    billing = models.ForeignKey(ProjectBilling, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    issued_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    paid_date = models.DateField(blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='draft')

    class Meta:
        verbose_name = 'Project Billing Invoice'
        verbose_name_plural = 'Project Billing Invoices'

    def __str__(self):
        return f"{self.billing.billing_number} - {self.invoice_number}"


# ---------------------------------------------------------------------------
# Project Costing
# ---------------------------------------------------------------------------

class ProjectCosting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='costings')
    budget = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    committed_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    forecasted_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    variance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    variance_pct = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    profitability_pct = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    contract_value = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Project Costing'
        verbose_name_plural = 'Project Costings'

    def __str__(self):
        return f"Costing - {self.project.code}"


class ProjectCostComponent(models.Model):
    costing = models.ForeignKey(ProjectCosting, on_delete=models.CASCADE, related_name='components')
    name = models.CharField(max_length=120, help_text='Labour, Material, Equipment, Subcontract...')
    budgeted = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    actual = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    committed = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Project Cost Component'
        verbose_name_plural = 'Project Cost Components'

    def __str__(self):
        return f"{self.costing.project.code} - {self.name}"
