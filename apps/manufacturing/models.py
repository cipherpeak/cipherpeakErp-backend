from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class CompanyStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class MachineStatus(models.TextChoices):
    OPERATIONAL = 'operational', 'Operational'
    MAINTENANCE = 'maintenance', 'Maintenance'
    BREAKDOWN = 'breakdown', 'Breakdown'
    IDLE = 'idle', 'Idle'


class BOMStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    ARCHIVED = 'archived', 'Archived'


class PlanStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PLANNED = 'planned', 'Planned'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class WOStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    PLANNED = 'planned', 'Planned'
    IN_PROGRESS = 'in_progress', 'In Progress'
    PAUSED = 'paused', 'Paused'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class PriorityLevel(models.TextChoices):
    LOW = 'low', 'Low'
    NORMAL = 'normal', 'Normal'
    HIGH = 'high', 'High'
    URGENT = 'urgent', 'Urgent'


# ---------------------------------------------------------------------------
# Machine Category
# ---------------------------------------------------------------------------

class MachineCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    machine_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Machine Category'
        verbose_name_plural = 'Machine Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Machine
# ---------------------------------------------------------------------------

class Machine(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        MachineCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='machines',
    )
    category_name = models.CharField(max_length=255, blank=True, null=True)
    plant = models.ForeignKey(
        'organization.Plant', on_delete=models.SET_NULL, blank=True, null=True, related_name='machines',
    )
    plant_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=MachineStatus.choices,
        default=MachineStatus.OPERATIONAL,
    )
    capacity_per_hour = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    efficiency_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    year_installed = models.IntegerField(blank=True, null=True)
    last_maintenance = models.DateField(blank=True, null=True)
    next_maintenance = models.DateField(blank=True, null=True)
    specs = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Machine'
        verbose_name_plural = 'Machines'
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if self.category and not self.category_name:
            self.category_name = self.category.name
        if self.plant and not self.plant_name:
            self.plant_name = self.plant.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Production Line
# ---------------------------------------------------------------------------

class ProductionLine(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        'organization.Plant', on_delete=models.SET_NULL, blank=True, null=True, related_name='production_lines',
    )
    plant_name = models.CharField(max_length=255, blank=True, null=True)
    capacity_per_hour = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    current_work_order = models.CharField(max_length=100, blank=True, null=True)
    efficiency_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    products_completed_today = models.IntegerField(default=0)
    supervisor = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Production Line'
        verbose_name_plural = 'Production Lines'
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if self.plant and not self.plant_name:
            self.plant_name = self.plant.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Work Center
# ---------------------------------------------------------------------------

class WorkCenter(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(
        'organization.Plant', on_delete=models.SET_NULL, blank=True, null=True, related_name='work_centers',
    )
    department = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cost_per_hour = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Work Center'
        verbose_name_plural = 'Work Centers'
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


# ---------------------------------------------------------------------------
# BOM Category
# ---------------------------------------------------------------------------

class BOMCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    bom_count = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=CompanyStatus.choices,
        default=CompanyStatus.ACTIVE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'BOM Category'
        verbose_name_plural = 'BOM Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Bill of Materials
# ---------------------------------------------------------------------------

class BillOfMaterial(models.Model):
    code = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='boms')
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_code = models.CharField(max_length=50, blank=True, null=True)
    version = models.CharField(max_length=20, default='1.0')
    status = models.CharField(
        max_length=20,
        choices=BOMStatus.choices,
        default=BOMStatus.DRAFT,
    )
    plant_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    total_material_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_operation_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bill of Materials'
        verbose_name_plural = 'Bills of Materials'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.product_name}"

    def save(self, *args, **kwargs):
        if self.product and not self.product_name:
            self.product_name = self.product.name
            self.product_code = self.product.code
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# BOM Material
# ---------------------------------------------------------------------------

class BOMMaterial(models.Model):
    bom = models.ForeignKey(BillOfMaterial, on_delete=models.CASCADE, related_name='bom_materials')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    substitute_available = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'BOM Material'
        verbose_name_plural = 'BOM Materials'

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.sku = self.item.sku
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# BOM Operation
# ---------------------------------------------------------------------------

class BOMOperation(models.Model):
    bom = models.ForeignKey(BillOfMaterial, on_delete=models.CASCADE, related_name='bom_operations')
    step_order = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    work_center = models.CharField(max_length=255, blank=True, null=True)
    time_hours = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cost_per_hour = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'BOM Operation'
        verbose_name_plural = 'BOM Operations'
        ordering = ['step_order']

    def __str__(self):
        return f"Step {self.step_order}: {self.name}"


# ---------------------------------------------------------------------------
# BOM Version
# ---------------------------------------------------------------------------

class BOMVersion(models.Model):
    bom = models.ForeignKey(BillOfMaterial, on_delete=models.CASCADE, related_name='versions')
    version = models.CharField(max_length=20)
    changed_by = models.CharField(max_length=255, blank=True, null=True)
    changes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'BOM Version'
        verbose_name_plural = 'BOM Versions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.bom.code} v{self.version}"


# ---------------------------------------------------------------------------
# BOM Substitution
# ---------------------------------------------------------------------------

class BOMSubstitution(models.Model):
    bom = models.ForeignKey(BillOfMaterial, on_delete=models.CASCADE, related_name='substitutions')
    original_item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE, related_name='bom_original_items')
    substitute_item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE, related_name='bom_substitute_items')
    reason = models.TextField(blank=True, null=True)
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default='proposed', help_text='proposed/approved/rejected')

    class Meta:
        verbose_name = 'BOM Substitution'
        verbose_name_plural = 'BOM Substitutions'

    def __str__(self):
        return f"{self.bom.code} - {self.original_item} -> {self.substitute_item}"


# ---------------------------------------------------------------------------
# Production Plan
# ---------------------------------------------------------------------------

class ProductionPlan(models.Model):
    plan_number = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='production_plans')
    product_name = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    priority = models.CharField(
        max_length=20,
        choices=PriorityLevel.choices,
        default=PriorityLevel.NORMAL,
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    production_line = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=PlanStatus.choices,
        default=PlanStatus.DRAFT,
    )
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Production Plan'
        verbose_name_plural = 'Production Plans'
        ordering = ['-created_at']

    def __str__(self):
        return self.plan_number

    def save(self, *args, **kwargs):
        if self.product and not self.product_name:
            self.product_name = self.product.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Production Plan Material
# ---------------------------------------------------------------------------

class ProductionPlanMaterial(models.Model):
    plan = models.ForeignKey(ProductionPlan, on_delete=models.CASCADE, related_name='plan_materials')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    required_qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    available_qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True, help_text='ok/shortage')

    class Meta:
        verbose_name = 'Production Plan Material'
        verbose_name_plural = 'Production Plan Materials'

    def __str__(self):
        return f"{self.item_name} - {self.plan.plan_number}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Work Order
# ---------------------------------------------------------------------------

class WorkOrder(models.Model):
    wo_number = models.CharField(max_length=50, unique=True)
    plan = models.ForeignKey(ProductionPlan, on_delete=models.SET_NULL, blank=True, null=True, related_name='work_orders')
    plan_number = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='work_orders')
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_code = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    produced_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rejected_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit = models.CharField(max_length=50, blank=True, null=True)
    priority = models.CharField(
        max_length=20,
        choices=PriorityLevel.choices,
        default=PriorityLevel.NORMAL,
    )
    status = models.CharField(
        max_length=20,
        choices=WOStatus.choices,
        default=WOStatus.DRAFT,
    )
    progress_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    production_line = models.CharField(max_length=255, blank=True, null=True)
    planned_start = models.DateTimeField(blank=True, null=True)
    planned_end = models.DateTimeField(blank=True, null=True)
    actual_start = models.DateTimeField(blank=True, null=True)
    actual_end = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
        ordering = ['-created_at']

    def __str__(self):
        return self.wo_number

    def save(self, *args, **kwargs):
        if self.plan and not self.plan_number:
            self.plan_number = self.plan.plan_number
        if self.product and not self.product_name:
            self.product_name = self.product.name
            self.product_code = self.product.code
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Work Order Material
# ---------------------------------------------------------------------------

class WorkOrderMaterial(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='wo_materials')
    item = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    required_qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    issued_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Work Order Material'
        verbose_name_plural = 'Work Order Materials'

    def __str__(self):
        return f"{self.item_name} - {self.wo.wo_number}"

    def save(self, *args, **kwargs):
        if self.item and not self.item_name:
            self.item_name = self.item.name
            self.sku = self.item.sku
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Work Order Operation
# ---------------------------------------------------------------------------

class WorkOrderOperation(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='wo_operations')
    step_order = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    work_center = models.CharField(max_length=255, blank=True, null=True)
    planned_hours = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    actual_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='pending')
    completed_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Work Order Operation'
        verbose_name_plural = 'Work Order Operations'
        ordering = ['step_order']

    def __str__(self):
        return f"Step {self.step_order}: {self.name}"


# ---------------------------------------------------------------------------
# Work Order Quality Check
# ---------------------------------------------------------------------------

class WorkOrderQualityCheck(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='quality_checks')
    check_name = models.CharField(max_length=255)
    result = models.CharField(max_length=100, blank=True, null=True)
    passed = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name = 'Work Order Quality Check'
        verbose_name_plural = 'Work Order Quality Checks'

    def __str__(self):
        return f"{self.wo.wo_number} - {self.check_name}"


# ---------------------------------------------------------------------------
# Job Card
# ---------------------------------------------------------------------------

class JobCard(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='job_cards')
    wo_number = models.CharField(max_length=50, blank=True, null=True)
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, blank=True, null=True, related_name='job_cards')
    machine_name = models.CharField(max_length=255, blank=True, null=True)
    operator = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending', help_text='pending/in_progress/completed/paused')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    produced_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rejected_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Job Card'
        verbose_name_plural = 'Job Cards'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.wo_number} - {self.machine_name}"

    def save(self, *args, **kwargs):
        if self.wo and not self.wo_number:
            self.wo_number = self.wo.wo_number
        if self.machine and not self.machine_name:
            self.machine_name = self.machine.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Production Tracking
# ---------------------------------------------------------------------------

class ProductionTracking(models.Model):
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='tracking')
    wo_number = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    shift = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True, help_text='on_track/delayed/completed')
    produced_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    actual_start = models.DateTimeField(blank=True, null=True)
    actual_end = models.DateTimeField(blank=True, null=True)
    downtime_min = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Production Tracking'
        verbose_name_plural = 'Production Tracking'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.wo_number} - {self.shift}"

    def save(self, *args, **kwargs):
        if self.wo and not self.wo_number:
            self.wo_number = self.wo.wo_number
        if self.wo and not self.product_name:
            self.product_name = self.wo.product_name
        super().save(*args, **kwargs)
