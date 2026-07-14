from typing import Dict, Any, List
from .models import (
    QualityCheck, DefectCategory, Inspection, InspectionChecklistItem,
    InspectionMeasurement, InspectionDefect, NCRRecord, CAPARecord, ReworkRecord,
)


# ===========================================================================
# QUALITY CHECK SERVICES
# ===========================================================================

def get_all_quality_checks() -> List[QualityCheck]:
    return QualityCheck.objects.filter(is_deleted=False).prefetch_related('products')

def create_quality_check(data: Dict[str, Any]) -> QualityCheck:
    check_code = data.get('check_code')
    if QualityCheck.objects.filter(check_code__iexact=check_code).exists():
        raise ValueError(f"Quality check with code '{check_code}' already exists.")
    products = data.pop('products', [])
    check = QualityCheck.objects.create(**data)
    if products:
        check.products.set(products)
    return check

def update_quality_check(check: QualityCheck, data: Dict[str, Any]) -> QualityCheck:
    check_code = data.get('check_code')
    if check_code and QualityCheck.objects.filter(check_code__iexact=check_code).exclude(id=check.id).exists():
        raise ValueError(f"Quality check with code '{check_code}' already exists.")
    products = data.pop('products', None)
    for field, value in data.items():
        setattr(check, field, value)
    check.save()
    if products is not None:
        check.products.set(products)
    return check

def delete_quality_check(check: QualityCheck) -> None:
    check.is_deleted = True
    check.save()


# ===========================================================================
# DEFECT CATEGORY SERVICES
# ===========================================================================

def get_all_defect_categories() -> List[DefectCategory]:
    return DefectCategory.objects.all()

def create_defect_category(data: Dict[str, Any]) -> DefectCategory:
    code = data.get('code')
    if DefectCategory.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Defect category with code '{code}' already exists.")
    return DefectCategory.objects.create(**data)

def update_defect_category(category: DefectCategory, data: Dict[str, Any]) -> DefectCategory:
    code = data.get('code')
    if code and DefectCategory.objects.filter(code__iexact=code).exclude(id=category.id).exists():
        raise ValueError(f"Defect category with code '{code}' already exists.")
    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    return category

def delete_defect_category(category: DefectCategory) -> None:
    category.delete()


# ===========================================================================
# INSPECTION SERVICES
# ===========================================================================

def get_all_inspections() -> List[Inspection]:
    return Inspection.objects.filter(is_deleted=False)

def get_inspection_with_details(inspection_id: int) -> Inspection:
    return Inspection.objects.prefetch_related(
        'checklist_items', 'measurements', 'defects',
    ).get(pk=inspection_id)

def create_inspection(data: Dict[str, Any]) -> Inspection:
    inspection_number = data.get('inspection_number')
    if Inspection.objects.filter(inspection_number__iexact=inspection_number).exists():
        raise ValueError(f"Inspection number '{inspection_number}' already exists.")
    checklist_data = data.pop('checklist_items', [])
    measurements_data = data.pop('measurements', [])
    defects_data = data.pop('defects', [])
    inspection = Inspection.objects.create(**data)
    for item_data in checklist_data:
        InspectionChecklistItem.objects.create(inspection=inspection, **item_data)
    for meas_data in measurements_data:
        InspectionMeasurement.objects.create(inspection=inspection, **meas_data)
    for defect_data in defects_data:
        InspectionDefect.objects.create(inspection=inspection, **defect_data)
    return inspection

def update_inspection(inspection: Inspection, data: Dict[str, Any]) -> Inspection:
    inspection_number = data.get('inspection_number')
    if inspection_number and Inspection.objects.filter(
        inspection_number__iexact=inspection_number,
    ).exclude(id=inspection.id).exists():
        raise ValueError(f"Inspection number '{inspection_number}' already exists.")
    data.pop('checklist_items', None)
    data.pop('measurements', None)
    data.pop('defects', None)
    for field, value in data.items():
        setattr(inspection, field, value)
    inspection.save()
    return inspection

def delete_inspection(inspection: Inspection) -> None:
    inspection.is_deleted = True
    inspection.save()


# ===========================================================================
# NCR RECORD SERVICES
# ===========================================================================

def get_all_ncr_records() -> List[NCRRecord]:
    return NCRRecord.objects.filter(is_deleted=False)

def create_ncr_record(data: Dict[str, Any]) -> NCRRecord:
    ncr_number = data.get('ncr_number')
    if NCRRecord.objects.filter(ncr_number__iexact=ncr_number).exists():
        raise ValueError(f"NCR number '{ncr_number}' already exists.")
    return NCRRecord.objects.create(**data)

def update_ncr_record(ncr: NCRRecord, data: Dict[str, Any]) -> NCRRecord:
    ncr_number = data.get('ncr_number')
    if ncr_number and NCRRecord.objects.filter(ncr_number__iexact=ncr_number).exclude(id=ncr.id).exists():
        raise ValueError(f"NCR number '{ncr_number}' already exists.")
    for field, value in data.items():
        setattr(ncr, field, value)
    ncr.save()
    return ncr

def delete_ncr_record(ncr: NCRRecord) -> None:
    ncr.is_deleted = True
    ncr.save()


# ===========================================================================
# CAPA RECORD SERVICES
# ===========================================================================

def get_all_capa_records() -> List[CAPARecord]:
    return CAPARecord.objects.filter(is_deleted=False)

def create_capa_record(data: Dict[str, Any]) -> CAPARecord:
    capa_number = data.get('capa_number')
    if CAPARecord.objects.filter(capa_number__iexact=capa_number).exists():
        raise ValueError(f"CAPA number '{capa_number}' already exists.")
    return CAPARecord.objects.create(**data)

def update_capa_record(capa: CAPARecord, data: Dict[str, Any]) -> CAPARecord:
    capa_number = data.get('capa_number')
    if capa_number and CAPARecord.objects.filter(capa_number__iexact=capa_number).exclude(id=capa.id).exists():
        raise ValueError(f"CAPA number '{capa_number}' already exists.")
    for field, value in data.items():
        setattr(capa, field, value)
    capa.save()
    return capa

def delete_capa_record(capa: CAPARecord) -> None:
    capa.is_deleted = True
    capa.save()


# ===========================================================================
# REWORK RECORD SERVICES
# ===========================================================================

def get_all_rework_records() -> List[ReworkRecord]:
    return ReworkRecord.objects.filter(is_deleted=False)

def create_rework_record(data: Dict[str, Any]) -> ReworkRecord:
    rework_number = data.get('rework_number')
    if ReworkRecord.objects.filter(rework_number__iexact=rework_number).exists():
        raise ValueError(f"Rework number '{rework_number}' already exists.")
    return ReworkRecord.objects.create(**data)

def update_rework_record(rework: ReworkRecord, data: Dict[str, Any]) -> ReworkRecord:
    rework_number = data.get('rework_number')
    if rework_number and ReworkRecord.objects.filter(
        rework_number__iexact=rework_number,
    ).exclude(id=rework.id).exists():
        raise ValueError(f"Rework number '{rework_number}' already exists.")
    for field, value in data.items():
        setattr(rework, field, value)
    rework.save()
    return rework

def delete_rework_record(rework: ReworkRecord) -> None:
    rework.is_deleted = True
    rework.save()
