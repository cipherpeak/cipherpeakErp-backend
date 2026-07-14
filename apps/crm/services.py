from typing import Dict, Any, List
from .models import (
    Account, Contact, Lead, Opportunity, CRMActivity, CRMQuotation, CRMQuotationLine,
)


# ===========================================================================
# ACCOUNT SERVICES
# ===========================================================================

def get_all_accounts() -> List[Account]:
    return Account.objects.filter(is_deleted=False)

def create_account(data: Dict[str, Any]) -> Account:
    account_number = data.get('account_number')
    if Account.objects.filter(account_number__iexact=account_number).exists():
        raise ValueError(f"Account number '{account_number}' already exists.")
    return Account.objects.create(**data)

def update_account(account: Account, data: Dict[str, Any]) -> Account:
    account_number = data.get('account_number')
    if account_number and Account.objects.filter(
        account_number__iexact=account_number,
    ).exclude(id=account.id).exists():
        raise ValueError(f"Account number '{account_number}' already exists.")
    for field, value in data.items():
        setattr(account, field, value)
    account.save()
    return account

def delete_account(account: Account) -> None:
    account.is_deleted = True
    account.save()


# ===========================================================================
# CONTACT SERVICES
# ===========================================================================

def get_all_contacts() -> List[Contact]:
    return Contact.objects.filter(is_deleted=False)

def create_contact(data: Dict[str, Any]) -> Contact:
    return Contact.objects.create(**data)

def update_contact(contact: Contact, data: Dict[str, Any]) -> Contact:
    for field, value in data.items():
        setattr(contact, field, value)
    contact.save()
    return contact

def delete_contact(contact: Contact) -> None:
    contact.is_deleted = True
    contact.save()


# ===========================================================================
# LEAD SERVICES
# ===========================================================================

def get_all_leads() -> List[Lead]:
    return Lead.objects.filter(is_deleted=False)

def create_lead(data: Dict[str, Any]) -> Lead:
    lead_number = data.get('lead_number')
    if Lead.objects.filter(lead_number__iexact=lead_number).exists():
        raise ValueError(f"Lead number '{lead_number}' already exists.")
    return Lead.objects.create(**data)

def update_lead(lead: Lead, data: Dict[str, Any]) -> Lead:
    lead_number = data.get('lead_number')
    if lead_number and Lead.objects.filter(lead_number__iexact=lead_number).exclude(id=lead.id).exists():
        raise ValueError(f"Lead number '{lead_number}' already exists.")
    for field, value in data.items():
        setattr(lead, field, value)
    lead.save()
    return lead

def delete_lead(lead: Lead) -> None:
    lead.is_deleted = True
    lead.save()


# ===========================================================================
# OPPORTUNITY SERVICES
# ===========================================================================

def get_all_opportunities() -> List[Opportunity]:
    return Opportunity.objects.filter(is_deleted=False)

def create_opportunity(data: Dict[str, Any]) -> Opportunity:
    opp_number = data.get('opp_number')
    if Opportunity.objects.filter(opp_number__iexact=opp_number).exists():
        raise ValueError(f"Opportunity number '{opp_number}' already exists.")
    return Opportunity.objects.create(**data)

def update_opportunity(opp: Opportunity, data: Dict[str, Any]) -> Opportunity:
    opp_number = data.get('opp_number')
    if opp_number and Opportunity.objects.filter(opp_number__iexact=opp_number).exclude(id=opp.id).exists():
        raise ValueError(f"Opportunity number '{opp_number}' already exists.")
    for field, value in data.items():
        setattr(opp, field, value)
    opp.save()
    return opp

def delete_opportunity(opp: Opportunity) -> None:
    opp.is_deleted = True
    opp.save()


# ===========================================================================
# CRM ACTIVITY SERVICES
# ===========================================================================

def get_all_activities() -> List[CRMActivity]:
    return CRMActivity.objects.filter(is_deleted=False)

def create_activity(data: Dict[str, Any]) -> CRMActivity:
    return CRMActivity.objects.create(**data)

def update_activity(activity: CRMActivity, data: Dict[str, Any]) -> CRMActivity:
    for field, value in data.items():
        setattr(activity, field, value)
    activity.save()
    return activity

def delete_activity(activity: CRMActivity) -> None:
    activity.is_deleted = True
    activity.save()


# ===========================================================================
# CRM QUOTATION SERVICES
# ===========================================================================

def get_all_quotations() -> List[CRMQuotation]:
    return CRMQuotation.objects.filter(is_deleted=False)

def get_quotation_with_lines(quotation_id: int) -> CRMQuotation:
    return CRMQuotation.objects.prefetch_related('lines').get(pk=quotation_id)

def create_quotation(data: Dict[str, Any]) -> CRMQuotation:
    quotation_number = data.get('quotation_number')
    if CRMQuotation.objects.filter(quotation_number__iexact=quotation_number).exists():
        raise ValueError(f"Quotation number '{quotation_number}' already exists.")
    lines_data = data.pop('lines', [])
    quotation = CRMQuotation.objects.create(**data)
    for line_data in lines_data:
        CRMQuotationLine.objects.create(quotation=quotation, **line_data)
    return quotation

def update_quotation(quotation: CRMQuotation, data: Dict[str, Any]) -> CRMQuotation:
    quotation_number = data.get('quotation_number')
    if quotation_number and CRMQuotation.objects.filter(
        quotation_number__iexact=quotation_number,
    ).exclude(id=quotation.id).exists():
        raise ValueError(f"Quotation number '{quotation_number}' already exists.")
    data.pop('lines', None)
    for field, value in data.items():
        setattr(quotation, field, value)
    quotation.save()
    return quotation

def delete_quotation(quotation: CRMQuotation) -> None:
    quotation.is_deleted = True
    quotation.save()
