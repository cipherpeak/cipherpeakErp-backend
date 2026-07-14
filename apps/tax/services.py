from typing import Dict, Any, List
from .models import (
    TaxJurisdiction, TaxType, HSNCode, TaxRate, TaxCategory,
    TaxGroup, TaxGroupMember, TaxRule, TaxRuleCondition,
    TaxExemption, ReverseChargeRecord, TaxReturn, TaxMappingRule,
)


# ===========================================================================
# TAX JURISDICTION SERVICES
# ===========================================================================

def get_all_jurisdictions() -> List[TaxJurisdiction]:
    return TaxJurisdiction.objects.filter(is_deleted=False)

def create_jurisdiction(data: Dict[str, Any]) -> TaxJurisdiction:
    return TaxJurisdiction.objects.create(**data)

def update_jurisdiction(jurisdiction: TaxJurisdiction, data: Dict[str, Any]) -> TaxJurisdiction:
    for field, value in data.items():
        setattr(jurisdiction, field, value)
    jurisdiction.save()
    return jurisdiction

def delete_jurisdiction(jurisdiction: TaxJurisdiction) -> None:
    jurisdiction.is_deleted = True
    jurisdiction.save()


# ===========================================================================
# TAX TYPE SERVICES
# ===========================================================================

def get_all_tax_types() -> List[TaxType]:
    return TaxType.objects.filter(is_deleted=False)

def create_tax_type(data: Dict[str, Any]) -> TaxType:
    code = data.get('code')
    if TaxType.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Tax type code '{code}' already exists.")
    return TaxType.objects.create(**data)

def update_tax_type(tax_type: TaxType, data: Dict[str, Any]) -> TaxType:
    code = data.get('code')
    if code and TaxType.objects.filter(code__iexact=code).exclude(id=tax_type.id).exists():
        raise ValueError(f"Tax type code '{code}' already exists.")
    for field, value in data.items():
        setattr(tax_type, field, value)
    tax_type.save()
    return tax_type

def delete_tax_type(tax_type: TaxType) -> None:
    tax_type.is_deleted = True
    tax_type.save()


# ===========================================================================
# HSN CODE SERVICES
# ===========================================================================

def get_all_hsn_codes() -> List[HSNCode]:
    return HSNCode.objects.filter(is_deleted=False)

def create_hsn_code(data: Dict[str, Any]) -> HSNCode:
    code = data.get('code')
    if HSNCode.objects.filter(code__iexact=code).exists():
        raise ValueError(f"HSN code '{code}' already exists.")
    return HSNCode.objects.create(**data)

def update_hsn_code(hsn: HSNCode, data: Dict[str, Any]) -> HSNCode:
    code = data.get('code')
    if code and HSNCode.objects.filter(code__iexact=code).exclude(id=hsn.id).exists():
        raise ValueError(f"HSN code '{code}' already exists.")
    for field, value in data.items():
        setattr(hsn, field, value)
    hsn.save()
    return hsn

def delete_hsn_code(hsn: HSNCode) -> None:
    hsn.is_deleted = True
    hsn.save()


# ===========================================================================
# TAX RATE SERVICES
# ===========================================================================

def get_all_tax_rates() -> List[TaxRate]:
    return TaxRate.objects.filter(is_deleted=False)

def create_tax_rate(data: Dict[str, Any]) -> TaxRate:
    code = data.get('code')
    if TaxRate.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Tax rate code '{code}' already exists.")
    return TaxRate.objects.create(**data)

def update_tax_rate(rate: TaxRate, data: Dict[str, Any]) -> TaxRate:
    code = data.get('code')
    if code and TaxRate.objects.filter(code__iexact=code).exclude(id=rate.id).exists():
        raise ValueError(f"Tax rate code '{code}' already exists.")
    for field, value in data.items():
        setattr(rate, field, value)
    rate.save()
    return rate

def delete_tax_rate(rate: TaxRate) -> None:
    rate.is_deleted = True
    rate.save()


# ===========================================================================
# TAX CATEGORY SERVICES
# ===========================================================================

def get_all_tax_categories() -> List[TaxCategory]:
    return TaxCategory.objects.filter(is_deleted=False)

def create_tax_category(data: Dict[str, Any]) -> TaxCategory:
    return TaxCategory.objects.create(**data)

def update_tax_category(category: TaxCategory, data: Dict[str, Any]) -> TaxCategory:
    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    return category

def delete_tax_category(category: TaxCategory) -> None:
    category.is_deleted = True
    category.save()


# ===========================================================================
# TAX GROUP SERVICES
# ===========================================================================

def get_all_tax_groups() -> List[TaxGroup]:
    return TaxGroup.objects.filter(is_deleted=False)

def get_tax_group_with_members(group_id: int) -> TaxGroup:
    return TaxGroup.objects.prefetch_related('members').get(pk=group_id)

def create_tax_group(data: Dict[str, Any]) -> TaxGroup:
    code = data.get('code')
    if TaxGroup.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Tax group code '{code}' already exists.")
    members_data = data.pop('members', [])
    group = TaxGroup.objects.create(**data)
    for member_data in members_data:
        TaxGroupMember.objects.create(group=group, **member_data)
    return group

def update_tax_group(group: TaxGroup, data: Dict[str, Any]) -> TaxGroup:
    code = data.get('code')
    if code and TaxGroup.objects.filter(code__iexact=code).exclude(id=group.id).exists():
        raise ValueError(f"Tax group code '{code}' already exists.")
    data.pop('members', None)
    for field, value in data.items():
        setattr(group, field, value)
    group.save()
    return group

def delete_tax_group(group: TaxGroup) -> None:
    group.is_deleted = True
    group.save()


# ===========================================================================
# TAX RULE SERVICES
# ===========================================================================

def get_all_tax_rules() -> List[TaxRule]:
    return TaxRule.objects.filter(is_deleted=False)

def get_tax_rule_with_conditions(rule_id: int) -> TaxRule:
    return TaxRule.objects.prefetch_related('conditions').get(pk=rule_id)

def create_tax_rule(data: Dict[str, Any]) -> TaxRule:
    code = data.get('code')
    if TaxRule.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Tax rule code '{code}' already exists.")
    conditions_data = data.pop('conditions', [])
    rule = TaxRule.objects.create(**data)
    for cond_data in conditions_data:
        TaxRuleCondition.objects.create(rule=rule, **cond_data)
    return rule

def update_tax_rule(rule: TaxRule, data: Dict[str, Any]) -> TaxRule:
    code = data.get('code')
    if code and TaxRule.objects.filter(code__iexact=code).exclude(id=rule.id).exists():
        raise ValueError(f"Tax rule code '{code}' already exists.")
    data.pop('conditions', None)
    for field, value in data.items():
        setattr(rule, field, value)
    rule.save()
    return rule

def delete_tax_rule(rule: TaxRule) -> None:
    rule.is_deleted = True
    rule.save()


# ===========================================================================
# TAX EXEMPTION SERVICES
# ===========================================================================

def get_all_exemptions() -> List[TaxExemption]:
    return TaxExemption.objects.filter(is_deleted=False)

def create_exemption(data: Dict[str, Any]) -> TaxExemption:
    certificate_number = data.get('certificate_number')
    if TaxExemption.objects.filter(certificate_number__iexact=certificate_number).exists():
        raise ValueError(f"Certificate number '{certificate_number}' already exists.")
    return TaxExemption.objects.create(**data)

def update_exemption(exemption: TaxExemption, data: Dict[str, Any]) -> TaxExemption:
    certificate_number = data.get('certificate_number')
    if certificate_number and TaxExemption.objects.filter(
        certificate_number__iexact=certificate_number,
    ).exclude(id=exemption.id).exists():
        raise ValueError(f"Certificate number '{certificate_number}' already exists.")
    for field, value in data.items():
        setattr(exemption, field, value)
    exemption.save()
    return exemption

def delete_exemption(exemption: TaxExemption) -> None:
    exemption.is_deleted = True
    exemption.save()


# ===========================================================================
# REVERSE CHARGE RECORD SERVICES
# ===========================================================================

def get_all_reverse_charge_records() -> List[ReverseChargeRecord]:
    return ReverseChargeRecord.objects.filter(is_deleted=False)

def create_reverse_charge_record(data: Dict[str, Any]) -> ReverseChargeRecord:
    return ReverseChargeRecord.objects.create(**data)

def update_reverse_charge_record(record: ReverseChargeRecord, data: Dict[str, Any]) -> ReverseChargeRecord:
    for field, value in data.items():
        setattr(record, field, value)
    record.save()
    return record

def delete_reverse_charge_record(record: ReverseChargeRecord) -> None:
    record.is_deleted = True
    record.save()


# ===========================================================================
# TAX RETURN SERVICES
# ===========================================================================

def get_all_tax_returns() -> List[TaxReturn]:
    return TaxReturn.objects.filter(is_deleted=False)

def create_tax_return(data: Dict[str, Any]) -> TaxReturn:
    return TaxReturn.objects.create(**data)

def update_tax_return(tax_return: TaxReturn, data: Dict[str, Any]) -> TaxReturn:
    for field, value in data.items():
        setattr(tax_return, field, value)
    tax_return.save()
    return tax_return

def delete_tax_return(tax_return: TaxReturn) -> None:
    tax_return.is_deleted = True
    tax_return.save()


# ===========================================================================
# TAX MAPPING RULE SERVICES
# ===========================================================================

def get_all_mapping_rules() -> List[TaxMappingRule]:
    return TaxMappingRule.objects.filter(is_deleted=False)

def create_mapping_rule(data: Dict[str, Any]) -> TaxMappingRule:
    return TaxMappingRule.objects.create(**data)

def update_mapping_rule(rule: TaxMappingRule, data: Dict[str, Any]) -> TaxMappingRule:
    for field, value in data.items():
        setattr(rule, field, value)
    rule.save()
    return rule

def delete_mapping_rule(rule: TaxMappingRule) -> None:
    rule.is_deleted = True
    rule.save()
