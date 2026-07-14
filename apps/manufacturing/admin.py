from django.contrib import admin
from .models import (
    MachineCategory, Machine, ProductionLine, WorkCenter, Product,
    BOMCategory, BillOfMaterial, BOMMaterial, BOMOperation, BOMVersion, BOMSubstitution,
    ProductionPlan, ProductionPlanMaterial, WorkOrder, WorkOrderMaterial,
    WorkOrderOperation, WorkOrderQualityCheck, JobCard, ProductionTracking,
)


@admin.register(MachineCategory)
class MachineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'machine_count', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category_name', 'plant_name', 'status', 'capacity_per_hour', 'efficiency_pct', 'last_maintenance', 'next_maintenance', 'created_at')
    search_fields = ('code', 'name', 'serial_number')
    list_filter = ('status', 'category')


@admin.register(ProductionLine)
class ProductionLineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'plant_name', 'status', 'capacity_per_hour', 'efficiency_pct', 'products_completed_today', 'supervisor', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('status',)


@admin.register(WorkCenter)
class WorkCenterAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'capacity', 'cost_per_hour', 'status', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('status',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'unit', 'status', 'cost_price', 'selling_price', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('status',)


@admin.register(BOMCategory)
class BOMCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'bom_count', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(BillOfMaterial)
class BillOfMaterialAdmin(admin.ModelAdmin):
    list_display = ('code', 'product_name', 'product_code', 'version', 'status', 'quantity', 'total_material_cost', 'total_operation_cost', 'total_cost', 'created_by', 'created_at')
    search_fields = ('code', 'product_name', 'product_code')
    list_filter = ('status',)


@admin.register(BOMMaterial)
class BOMMaterialAdmin(admin.ModelAdmin):
    list_display = ('bom', 'item_name', 'sku', 'quantity', 'unit', 'unit_cost', 'total_cost', 'substitute_available')
    search_fields = ('item_name', 'sku')


@admin.register(BOMOperation)
class BOMOperationAdmin(admin.ModelAdmin):
    list_display = ('bom', 'step_order', 'name', 'work_center', 'time_hours', 'cost_per_hour', 'total_cost')
    search_fields = ('name',)


@admin.register(BOMVersion)
class BOMVersionAdmin(admin.ModelAdmin):
    list_display = ('bom', 'version', 'changed_by', 'changes', 'created_at')
    search_fields = ('version',)


@admin.register(BOMSubstitution)
class BOMSubstitutionAdmin(admin.ModelAdmin):
    list_display = ('bom', 'original_item', 'substitute_item', 'reason', 'approved_by', 'status')
    search_fields = ('reason',)
    list_filter = ('status',)


@admin.register(ProductionPlan)
class ProductionPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_number', 'product_name', 'quantity', 'priority', 'start_date', 'end_date', 'production_line', 'status', 'created_by', 'created_at')
    search_fields = ('plan_number', 'product_name')
    list_filter = ('status', 'priority')


@admin.register(ProductionPlanMaterial)
class ProductionPlanMaterialAdmin(admin.ModelAdmin):
    list_display = ('plan', 'item_name', 'required_qty', 'available_qty', 'status')
    search_fields = ('item_name',)


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('wo_number', 'plan_number', 'product_name', 'product_code', 'quantity', 'produced_qty', 'rejected_qty', 'priority', 'status', 'progress_pct', 'production_line', 'created_at')
    search_fields = ('wo_number', 'product_name', 'product_code')
    list_filter = ('status', 'priority')


@admin.register(WorkOrderMaterial)
class WorkOrderMaterialAdmin(admin.ModelAdmin):
    list_display = ('wo', 'item_name', 'sku', 'required_qty', 'issued_qty', 'unit', 'unit_cost')
    search_fields = ('item_name', 'sku')


@admin.register(WorkOrderOperation)
class WorkOrderOperationAdmin(admin.ModelAdmin):
    list_display = ('wo', 'step_order', 'name', 'work_center', 'planned_hours', 'actual_hours', 'status', 'completed_by')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(WorkOrderQualityCheck)
class WorkOrderQualityCheckAdmin(admin.ModelAdmin):
    list_display = ('wo', 'check_name', 'result', 'passed')
    search_fields = ('check_name',)
    list_filter = ('passed',)


@admin.register(JobCard)
class JobCardAdmin(admin.ModelAdmin):
    list_display = ('wo_number', 'machine_name', 'operator', 'status', 'start_time', 'end_time', 'produced_qty', 'rejected_qty', 'created_at')
    search_fields = ('wo_number', 'machine_name', 'operator')
    list_filter = ('status',)


@admin.register(ProductionTracking)
class ProductionTrackingAdmin(admin.ModelAdmin):
    list_display = ('wo_number', 'product_name', 'shift', 'status', 'produced_qty', 'target_qty', 'actual_start', 'actual_end', 'downtime_min', 'created_at')
    search_fields = ('wo_number', 'product_name')
    list_filter = ('status', 'shift')
