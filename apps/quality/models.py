from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class ActiveInactive(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class CheckCategory(models.TextChoices):
    DIMENSIONAL = 'dimensional', 'Dimensional'
    VISUAL = 'visual', 'Visual'
    CHEMICAL = 'chemical', 'Chemical'
    FUNCTIONAL = 'functional', 'Functional'
    MATERIAL = 'material', 'Material'


class CheckFrequency(models.TextChoices):
    HOURLY = 'hourly', 'Hourly'
    PER_SHIFT = 'per_shift', 'Per Shift'
    PER_BATCH = 'per_batch', 'Per Batch'
    DAILY = 'daily', 'Daily'
    WEEKLY = 'weekly', 'Weekly'


class InspectionType(models.TextChoices):
    INCOMING = 'incoming', 'Incoming'
    IN_PROCESS = 'in_process', 'In Process'
    FINAL = 'final', 'Final'
    AUDIT = 'audit', 'Audit'


class InspectionStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    PASSED = 'passed', 'Passed'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'


class NCRStatus(models.TextChoices):
    OPEN = 'open', 'Open'
    UNDER_REVIEW = 'under_review', 'Under Review'
    RESOLVED = 'resolved', 'Resolved'
    CLOSED = 'closed', 'Closed'


class CAPAType(models.TextChoices):
    CORRECTIVE = 'corrective', 'Corrective'
    PREVENTIVE = 'preventive', 'Preventive'


class CAPAStatus(models.TextChoices):
    OPEN = 'open', 'Open'
    IN_PROGRESS = 'in_progress', 'In Progress'
    VERIFICATION = 'verification', 'Verification'
    CLOSED = 'closed', 'Closed'
    CANCELLED = 'cancelled', 'Cancelled'


class ReworkStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    SCRAPPED = 'scrapped', 'Scrapped'


# ---------------------------------------------------------------------------
# Quality Check Template
# ---------------------------------------------------------------------------

class QualityCheck(models.Model):
    check_code = models.CharField(max_length=30, unique=True)
    parameter = models.CharField(max_length=300)
    category = models.CharField(max_length=20, choices=CheckCategory.choices)
    standard_value = models.CharField(max_length=200, blank=True, null=True)
    tolerance = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    frequency = models.CharField(
        max_length=20,
        choices=CheckFrequency.choices,
        default=CheckFrequency.PER_BATCH,
    )
    measurement_method = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ActiveInactive.choices,
        default=ActiveInactive.ACTIVE,
    )
    products = models.ManyToManyField(
        'manufacturing.Product', blank=True, related_name='quality_checks',
    )
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_quality_checks',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Quality Check'
        verbose_name_plural = 'Quality Checks'
        ordering = ['check_code']

    def __str__(self):
        return f"{self.check_code} - {self.parameter}"


# ---------------------------------------------------------------------------
# Defect Category
# ---------------------------------------------------------------------------

class DefectCategory(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Defect Category'
        verbose_name_plural = 'Defect Categories'
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


# ---------------------------------------------------------------------------
# Inspection
# ---------------------------------------------------------------------------

class Inspection(models.Model):
    inspection_number = models.CharField(max_length=30, unique=True)
    wo = models.ForeignKey(
        'manufacturing.WorkOrder', on_delete=models.SET_NULL, blank=True, null=True, related_name='inspections',
    )
    wo_number = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(
        'manufacturing.Product', on_delete=models.CASCADE, related_name='inspections',
    )
    product_name = models.CharField(max_length=255, blank=True, null=True)
    inspection_type = models.CharField(max_length=20, choices=InspectionType.choices)
    inspector = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='inspections',
    )
    inspector_name = models.CharField(max_length=255, blank=True, null=True)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    batch_size = models.IntegerField(blank=True, null=True)
    sample_size = models.IntegerField(blank=True, null=True)
    accepted_qty = models.IntegerField(default=0)
    rejected_qty = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=InspectionStatus.choices,
        default=InspectionStatus.PENDING,
    )
    date = models.DateField(auto_now_add=False, null=True, blank=True)
    time_started = models.TimeField(blank=True, null=True)
    time_completed = models.TimeField(blank=True, null=True)
    production_line = models.ForeignKey(
        'manufacturing.ProductionLine', on_delete=models.SET_NULL, blank=True, null=True, related_name='inspections',
    )
    production_line_name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Inspection'
        verbose_name_plural = 'Inspections'
        ordering = ['-created_at']

    def __str__(self):
        return self.inspection_number

    def save(self, *args, **kwargs):
        if self.wo and not self.wo_number:
            self.wo_number = self.wo.wo_number
        if self.product and not self.product_name:
            self.product_name = self.product.name
        if self.production_line and not self.production_line_name:
            self.production_line_name = self.production_line.name
        super().save(*args, **kwargs)


class InspectionChecklistItem(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='checklist_items')
    check_code = models.CharField(max_length=30, blank=True, null=True)
    parameter = models.CharField(max_length=300, blank=True, null=True)
    standard = models.CharField(max_length=200, blank=True, null=True)
    actual_value = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=10, default='pass', help_text='pass/fail/na')
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Inspection Checklist Item'
        verbose_name_plural = 'Inspection Checklist Items'

    def __str__(self):
        return f"{self.inspection.inspection_number} - {self.parameter}"


class InspectionMeasurement(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='measurements')
    parameter = models.CharField(max_length=300, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    nominal = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    usl = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    lsl = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    readings = models.JSONField(default=list, blank=True)
    mean_value = models.DecimalField(max_digits=15, decimal_places=4, blank=True, null=True)
    within_spec = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Inspection Measurement'
        verbose_name_plural = 'Inspection Measurements'

    def __str__(self):
        return f"{self.inspection.inspection_number} - {self.parameter}"


class InspectionDefect(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='defects')
    defect_code = models.CharField(max_length=30, blank=True, null=True)
    defect_category = models.ForeignKey(
        DefectCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='inspection_defects',
    )
    description = models.TextField(blank=True, null=True)
    qty_defective = models.IntegerField(default=0)
    severity = models.CharField(max_length=20, default='major', help_text='minor/major/critical')
    location = models.CharField(max_length=200, blank=True, null=True)
    disposition = models.CharField(max_length=30, default='rework', help_text='rework/scrap/use_as_is/return')

    class Meta:
        verbose_name = 'Inspection Defect'
        verbose_name_plural = 'Inspection Defects'

    def __str__(self):
        return f"{self.inspection.inspection_number} - {self.defect_code}"


# ---------------------------------------------------------------------------
# NCR (Non-Conformance Report)
# ---------------------------------------------------------------------------

class NCRRecord(models.Model):
    ncr_number = models.CharField(max_length=30, unique=True)
    inspection = models.ForeignKey(
        Inspection, on_delete=models.SET_NULL, blank=True, null=True, related_name='ncr_records',
    )
    product = models.ForeignKey(
        'manufacturing.Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='ncr_records',
    )
    product_name = models.CharField(max_length=255, blank=True, null=True)
    severity = models.CharField(max_length=20, default='major', help_text='minor/major/critical')
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    root_cause = models.TextField(blank=True, null=True)
    immediate_action = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=NCRStatus.choices,
        default=NCRStatus.OPEN,
    )
    raised_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='raised_ncrs',
    )
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_ncrs',
    )
    closed_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='closed_ncrs',
    )
    closed_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'NCR Record'
        verbose_name_plural = 'NCR Records'
        ordering = ['-created_at']

    def __str__(self):
        return self.ncr_number

    def save(self, *args, **kwargs):
        if self.product and not self.product_name:
            self.product_name = self.product.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# CAPA (Corrective and Preventive Action)
# ---------------------------------------------------------------------------

class CAPARecord(models.Model):
    capa_number = models.CharField(max_length=30, unique=True)
    ncr = models.ForeignKey(
        NCRRecord, on_delete=models.SET_NULL, blank=True, null=True, related_name='capa_records',
    )
    type = models.CharField(
        max_length=20,
        choices=CAPAType.choices,
        default=CAPAType.CORRECTIVE,
    )
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    root_cause = models.TextField(blank=True, null=True)
    action_plan = models.TextField(blank=True, null=True)
    target_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CAPAStatus.choices,
        default=CAPAStatus.OPEN,
    )
    owner = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='owned_capas',
    )
    verified_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='verified_capas',
    )
    verified_at = models.DateTimeField(blank=True, null=True)
    effectiveness = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='created_capas',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'CAPA Record'
        verbose_name_plural = 'CAPA Records'
        ordering = ['-created_at']

    def __str__(self):
        return self.capa_number


# ---------------------------------------------------------------------------
# Rework Record
# ---------------------------------------------------------------------------

class ReworkRecord(models.Model):
    rework_number = models.CharField(max_length=30, unique=True)
    ncr = models.ForeignKey(
        NCRRecord, on_delete=models.SET_NULL, blank=True, null=True, related_name='rework_records',
    )
    wo = models.ForeignKey(
        'manufacturing.WorkOrder', on_delete=models.SET_NULL, blank=True, null=True, related_name='rework_records',
    )
    product = models.ForeignKey(
        'manufacturing.Product', on_delete=models.CASCADE, related_name='rework_records',
    )
    product_name = models.CharField(max_length=255, blank=True, null=True)
    qty = models.DecimalField(max_digits=15, decimal_places=3)
    rework_reason = models.TextField(blank=True, null=True)
    rework_steps = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_reworks',
    )
    status = models.CharField(
        max_length=20,
        choices=ReworkStatus.choices,
        default=ReworkStatus.PENDING,
    )
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rework Record'
        verbose_name_plural = 'Rework Records'
        ordering = ['-created_at']

    def __str__(self):
        return self.rework_number

    def save(self, *args, **kwargs):
        if self.product and not self.product_name:
            self.product_name = self.product.name
        super().save(*args, **kwargs)
