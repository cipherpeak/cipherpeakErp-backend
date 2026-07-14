from django.db import transaction
from typing import Dict, Any, List
from .models import (
    MachineCategory, Machine, ProductionLine, WorkCenter, Product,
    BOMCategory, BillOfMaterial, BOMMaterial, BOMOperation, BOMVersion, BOMSubstitution,
    ProductionPlan, ProductionPlanMaterial, WorkOrder, WorkOrderMaterial,
    WorkOrderOperation, WorkOrderQualityCheck, JobCard, ProductionTracking,
)


# ===========================================================================
# MACHINE CATEGORY SERVICES
# ===========================================================================

def get_all_machine_categories() -> List[MachineCategory]:
    return MachineCategory.objects.all()

def create_machine_category(data: Dict[str, Any]) -> MachineCategory:
    name = data.get('name')
    if MachineCategory.objects.filter(name__iexact=name).exists():
        raise ValueError(f"Machine category with name '{name}' already exists.")
    return MachineCategory.objects.create(**data)

def update_machine_category(category: MachineCategory, data: Dict[str, Any]) -> MachineCategory:
    name = data.get('name')
    if name and MachineCategory.objects.filter(name__iexact=name).exclude(id=category.id).exists():
        raise ValueError(f"Machine category with name '{name}' already exists.")
    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    return category

def delete_machine_category(category: MachineCategory) -> None:
    category.delete()


# ===========================================================================
# MACHINE SERVICES
# ===========================================================================

def get_all_machines() -> List[Machine]:
    return Machine.objects.all()

def create_machine(data: Dict[str, Any]) -> Machine:
    code = data.get('code')
    if Machine.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Machine with code '{code}' already exists.")
    return Machine.objects.create(**data)

def update_machine(machine: Machine, data: Dict[str, Any]) -> Machine:
    code = data.get('code')
    if code and Machine.objects.filter(code__iexact=code).exclude(id=machine.id).exists():
        raise ValueError(f"Machine with code '{code}' already exists.")
    for field, value in data.items():
        setattr(machine, field, value)
    machine.save()
    return machine

def delete_machine(machine: Machine) -> None:
    machine.delete()


# ===========================================================================
# PRODUCTION LINE SERVICES
# ===========================================================================

def get_all_production_lines() -> List[ProductionLine]:
    return ProductionLine.objects.all()

def create_production_line(data: Dict[str, Any]) -> ProductionLine:
    code = data.get('code')
    if ProductionLine.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Production line with code '{code}' already exists.")
    return ProductionLine.objects.create(**data)

def update_production_line(line: ProductionLine, data: Dict[str, Any]) -> ProductionLine:
    code = data.get('code')
    if code and ProductionLine.objects.filter(code__iexact=code).exclude(id=line.id).exists():
        raise ValueError(f"Production line with code '{code}' already exists.")
    for field, value in data.items():
        setattr(line, field, value)
    line.save()
    return line

def delete_production_line(line: ProductionLine) -> None:
    line.delete()


# ===========================================================================
# WORK CENTER SERVICES
# ===========================================================================

def get_all_work_centers() -> List[WorkCenter]:
    return WorkCenter.objects.all()

def create_work_center(data: Dict[str, Any]) -> WorkCenter:
    code = data.get('code')
    if WorkCenter.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Work center with code '{code}' already exists.")
    return WorkCenter.objects.create(**data)

def update_work_center(center: WorkCenter, data: Dict[str, Any]) -> WorkCenter:
    code = data.get('code')
    if code and WorkCenter.objects.filter(code__iexact=code).exclude(id=center.id).exists():
        raise ValueError(f"Work center with code '{code}' already exists.")
    for field, value in data.items():
        setattr(center, field, value)
    center.save()
    return center

def delete_work_center(center: WorkCenter) -> None:
    center.delete()


# ===========================================================================
# PRODUCT SERVICES
# ===========================================================================

def get_all_products() -> List[Product]:
    return Product.objects.all()

def create_product(data: Dict[str, Any]) -> Product:
    code = data.get('code')
    if Product.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Product with code '{code}' already exists.")
    return Product.objects.create(**data)

def update_product(product: Product, data: Dict[str, Any]) -> Product:
    code = data.get('code')
    if code and Product.objects.filter(code__iexact=code).exclude(id=product.id).exists():
        raise ValueError(f"Product with code '{code}' already exists.")
    for field, value in data.items():
        setattr(product, field, value)
    product.save()
    return product

def delete_product(product: Product) -> None:
    product.delete()


# ===========================================================================
# BOM CATEGORY SERVICES
# ===========================================================================

def get_all_bom_categories() -> List[BOMCategory]:
    return BOMCategory.objects.all()

def create_bom_category(data: Dict[str, Any]) -> BOMCategory:
    name = data.get('name')
    if BOMCategory.objects.filter(name__iexact=name).exists():
        raise ValueError(f"BOM category with name '{name}' already exists.")
    return BOMCategory.objects.create(**data)

def update_bom_category(category: BOMCategory, data: Dict[str, Any]) -> BOMCategory:
    name = data.get('name')
    if name and BOMCategory.objects.filter(name__iexact=name).exclude(id=category.id).exists():
        raise ValueError(f"BOM category with name '{name}' already exists.")
    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    return category

def delete_bom_category(category: BOMCategory) -> None:
    category.delete()


# ===========================================================================
# BILL OF MATERIALS SERVICES
# ===========================================================================

def get_all_boms() -> List[BillOfMaterial]:
    return BillOfMaterial.objects.all()

def get_bom_with_details(bom_id: int) -> BillOfMaterial:
    return BillOfMaterial.objects.prefetch_related('bom_materials', 'bom_operations').get(pk=bom_id)

def create_bom(data: Dict[str, Any]) -> BillOfMaterial:
    code = data.get('code')
    if BillOfMaterial.objects.filter(code__iexact=code).exists():
        raise ValueError(f"BOM with code '{code}' already exists.")
    materials_data = data.pop('bom_materials', [])
    operations_data = data.pop('bom_operations', [])
    bom = BillOfMaterial.objects.create(**data)
    for mat_data in materials_data:
        BOMMaterial.objects.create(bom=bom, **mat_data)
    for op_data in operations_data:
        BOMOperation.objects.create(bom=bom, **op_data)
    return bom

def update_bom(bom: BillOfMaterial, data: Dict[str, Any]) -> BillOfMaterial:
    for field, value in data.items():
        setattr(bom, field, value)
    bom.save()
    return bom

def delete_bom(bom: BillOfMaterial) -> None:
    bom.delete()


# ===========================================================================
# BOM VERSION SERVICES
# ===========================================================================

def get_all_bom_versions() -> List[BOMVersion]:
    return BOMVersion.objects.all()

def create_bom_version(data: Dict[str, Any]) -> BOMVersion:
    return BOMVersion.objects.create(**data)

def delete_bom_version(version: BOMVersion) -> None:
    version.delete()


# ===========================================================================
# BOM SUBSTITUTION SERVICES
# ===========================================================================

def get_all_bom_substitutions() -> List[BOMSubstitution]:
    return BOMSubstitution.objects.all()

def create_bom_substitution(data: Dict[str, Any]) -> BOMSubstitution:
    return BOMSubstitution.objects.create(**data)

def update_bom_substitution(sub: BOMSubstitution, data: Dict[str, Any]) -> BOMSubstitution:
    for field, value in data.items():
        setattr(sub, field, value)
    sub.save()
    return sub

def delete_bom_substitution(sub: BOMSubstitution) -> None:
    sub.delete()


# ===========================================================================
# PRODUCTION PLAN SERVICES
# ===========================================================================

def get_all_production_plans() -> List[ProductionPlan]:
    return ProductionPlan.objects.all()

def get_production_plan_with_materials(plan_id: int) -> ProductionPlan:
    return ProductionPlan.objects.prefetch_related('plan_materials').get(pk=plan_id)

def create_production_plan(data: Dict[str, Any]) -> ProductionPlan:
    plan_number = data.get('plan_number')
    if ProductionPlan.objects.filter(plan_number__iexact=plan_number).exists():
        raise ValueError(f"Plan number '{plan_number}' already exists.")
    materials_data = data.pop('plan_materials', [])
    plan = ProductionPlan.objects.create(**data)
    for mat_data in materials_data:
        ProductionPlanMaterial.objects.create(plan=plan, **mat_data)
    return plan

def update_production_plan(plan: ProductionPlan, data: Dict[str, Any]) -> ProductionPlan:
    for field, value in data.items():
        setattr(plan, field, value)
    plan.save()
    return plan

def delete_production_plan(plan: ProductionPlan) -> None:
    plan.delete()


# ===========================================================================
# WORK ORDER SERVICES
# ===========================================================================

def get_all_work_orders() -> List[WorkOrder]:
    return WorkOrder.objects.all()

def get_work_order_with_details(wo_id: int) -> WorkOrder:
    return WorkOrder.objects.prefetch_related('wo_materials', 'wo_operations', 'quality_checks').get(pk=wo_id)

def create_work_order(data: Dict[str, Any]) -> WorkOrder:
    wo_number = data.get('wo_number')
    if WorkOrder.objects.filter(wo_number__iexact=wo_number).exists():
        raise ValueError(f"Work order number '{wo_number}' already exists.")
    materials_data = data.pop('wo_materials', [])
    operations_data = data.pop('wo_operations', [])
    checks_data = data.pop('quality_checks', [])
    wo = WorkOrder.objects.create(**data)
    for mat_data in materials_data:
        WorkOrderMaterial.objects.create(wo=wo, **mat_data)
    for op_data in operations_data:
        WorkOrderOperation.objects.create(wo=wo, **op_data)
    for check_data in checks_data:
        WorkOrderQualityCheck.objects.create(wo=wo, **check_data)
    return wo

def update_work_order(wo: WorkOrder, data: Dict[str, Any]) -> WorkOrder:
    for field, value in data.items():
        setattr(wo, field, value)
    wo.save()
    return wo

def delete_work_order(wo: WorkOrder) -> None:
    wo.delete()


# ===========================================================================
# JOB CARD SERVICES
# ===========================================================================

def get_all_job_cards() -> List[JobCard]:
    return JobCard.objects.all()

def create_job_card(data: Dict[str, Any]) -> JobCard:
    return JobCard.objects.create(**data)

def update_job_card(card: JobCard, data: Dict[str, Any]) -> JobCard:
    for field, value in data.items():
        setattr(card, field, value)
    card.save()
    return card

def delete_job_card(card: JobCard) -> None:
    card.delete()


# ===========================================================================
# PRODUCTION TRACKING SERVICES
# ===========================================================================

def get_all_production_tracking() -> List[ProductionTracking]:
    return ProductionTracking.objects.all()

def create_production_tracking(data: Dict[str, Any]) -> ProductionTracking:
    return ProductionTracking.objects.create(**data)

def update_production_tracking(tracking: ProductionTracking, data: Dict[str, Any]) -> ProductionTracking:
    for field, value in data.items():
        setattr(tracking, field, value)
    tracking.save()
    return tracking

def delete_production_tracking(tracking: ProductionTracking) -> None:
    tracking.delete()
