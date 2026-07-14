from django.db import transaction
from typing import Dict, Any, List
from .models import (
    VendorCategory, PaymentTerm, Vendor, VendorContact,
    PurchaseRequest, PurchaseRequestItem, RFQ, RFQVendor, RFQItem,
    Quotation, QuotationItem, PurchaseOrder, PurchaseOrderItem,
    GRN, GRNItem, PurchaseInvoice, PurchaseInvoiceItem, VendorPayment,
)


# ===========================================================================
# VENDOR CATEGORY SERVICES
# ===========================================================================

def get_all_vendor_categories() -> List[VendorCategory]:
    return VendorCategory.objects.all()

def create_vendor_category(data: Dict[str, Any]) -> VendorCategory:
    name = data.get('name')
    if VendorCategory.objects.filter(name__iexact=name).exists():
        raise ValueError(f"Vendor category with name '{name}' already exists.")
    return VendorCategory.objects.create(**data)

def update_vendor_category(category: VendorCategory, data: Dict[str, Any]) -> VendorCategory:
    name = data.get('name')
    if name and VendorCategory.objects.filter(name__iexact=name).exclude(id=category.id).exists():
        raise ValueError(f"Vendor category with name '{name}' already exists.")
    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    return category

def delete_vendor_category(category: VendorCategory) -> None:
    category.delete()


# ===========================================================================
# PAYMENT TERMS SERVICES
# ===========================================================================

def get_all_payment_terms() -> List[PaymentTerm]:
    return PaymentTerm.objects.all()

def create_payment_term(data: Dict[str, Any]) -> PaymentTerm:
    name = data.get('name')
    if PaymentTerm.objects.filter(name__iexact=name).exists():
        raise ValueError(f"Payment term with name '{name}' already exists.")
    return PaymentTerm.objects.create(**data)

def update_payment_term(term: PaymentTerm, data: Dict[str, Any]) -> PaymentTerm:
    name = data.get('name')
    if name and PaymentTerm.objects.filter(name__iexact=name).exclude(id=term.id).exists():
        raise ValueError(f"Payment term with name '{name}' already exists.")
    for field, value in data.items():
        setattr(term, field, value)
    term.save()
    return term

def delete_payment_term(term: PaymentTerm) -> None:
    term.delete()


# ===========================================================================
# VENDOR SERVICES
# ===========================================================================

def get_all_vendors() -> List[Vendor]:
    return Vendor.objects.all()

def create_vendor(data: Dict[str, Any]) -> Vendor:
    code = data.get('code')
    if Vendor.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Vendor with code '{code}' already exists.")
    contacts_data = data.pop('contacts', [])
    vendor = Vendor.objects.create(**data)
    for contact_data in contacts_data:
        VendorContact.objects.create(vendor=vendor, **contact_data)
    return vendor

def update_vendor(vendor: Vendor, data: Dict[str, Any]) -> Vendor:
    code = data.get('code')
    if code and Vendor.objects.filter(code__iexact=code).exclude(id=vendor.id).exists():
        raise ValueError(f"Vendor with code '{code}' already exists.")
    for field, value in data.items():
        setattr(vendor, field, value)
    vendor.save()
    return vendor

def delete_vendor(vendor: Vendor) -> None:
    vendor.delete()


# ===========================================================================
# VENDOR CONTACT SERVICES
# ===========================================================================

def get_vendor_contacts(vendor_id: int) -> List[VendorContact]:
    return VendorContact.objects.filter(vendor_id=vendor_id)

def create_vendor_contact(data: Dict[str, Any]) -> VendorContact:
    return VendorContact.objects.create(**data)

def update_vendor_contact(contact: VendorContact, data: Dict[str, Any]) -> VendorContact:
    for field, value in data.items():
        setattr(contact, field, value)
    contact.save()
    return contact

def delete_vendor_contact(contact: VendorContact) -> None:
    contact.delete()


# ===========================================================================
# PURCHASE REQUEST SERVICES
# ===========================================================================

def get_all_purchase_requests() -> List[PurchaseRequest]:
    return PurchaseRequest.objects.all()

def get_purchase_request_with_items(pr_id: int) -> PurchaseRequest:
    return PurchaseRequest.objects.prefetch_related('pr_items').get(pk=pr_id)

def create_purchase_request(data: Dict[str, Any]) -> PurchaseRequest:
    pr_number = data.get('pr_number')
    if PurchaseRequest.objects.filter(pr_number__iexact=pr_number).exists():
        raise ValueError(f"PR number '{pr_number}' already exists.")
    items_data = data.pop('items', [])
    pr = PurchaseRequest.objects.create(**data)
    for item_data in items_data:
        PurchaseRequestItem.objects.create(pr=pr, **item_data)
    return pr

def update_purchase_request(pr: PurchaseRequest, data: Dict[str, Any]) -> PurchaseRequest:
    for field, value in data.items():
        setattr(pr, field, value)
    pr.save()
    return pr

def delete_purchase_request(pr: PurchaseRequest) -> None:
    pr.delete()


# ===========================================================================
# RFQ SERVICES
# ===========================================================================

def get_all_rfqs() -> List[RFQ]:
    return RFQ.objects.all()

def get_rfq_with_details(rfq_id: int) -> RFQ:
    return RFQ.objects.prefetch_related('rfq_vendors', 'rfq_items').get(pk=rfq_id)

def create_rfq(data: Dict[str, Any]) -> RFQ:
    rfq_number = data.get('rfq_number')
    if RFQ.objects.filter(rfq_number__iexact=rfq_number).exists():
        raise ValueError(f"RFQ number '{rfq_number}' already exists.")
    vendors_data = data.pop('rfq_vendors', [])
    items_data = data.pop('rfq_items', [])
    rfq = RFQ.objects.create(**data)
    for v_data in vendors_data:
        RFQVendor.objects.create(rfq=rfq, **v_data)
    for i_data in items_data:
        RFQItem.objects.create(rfq=rfq, **i_data)
    return rfq

def update_rfq(rfq: RFQ, data: Dict[str, Any]) -> RFQ:
    for field, value in data.items():
        setattr(rfq, field, value)
    rfq.save()
    return rfq

def delete_rfq(rfq: RFQ) -> None:
    rfq.delete()


# ===========================================================================
# QUOTATION SERVICES
# ===========================================================================

def get_all_quotations() -> List[Quotation]:
    return Quotation.objects.all()

def get_quotation_with_items(quotation_id: int) -> Quotation:
    return Quotation.objects.prefetch_related('quotation_items').get(pk=quotation_id)

def create_quotation(data: Dict[str, Any]) -> Quotation:
    quotation_number = data.get('quotation_number')
    if Quotation.objects.filter(quotation_number__iexact=quotation_number).exists():
        raise ValueError(f"Quotation number '{quotation_number}' already exists.")
    items_data = data.pop('quotation_items', [])
    quotation = Quotation.objects.create(**data)
    for item_data in items_data:
        QuotationItem.objects.create(quotation=quotation, **item_data)
    return quotation

def update_quotation(quotation: Quotation, data: Dict[str, Any]) -> Quotation:
    for field, value in data.items():
        setattr(quotation, field, value)
    quotation.save()
    return quotation

def delete_quotation(quotation: Quotation) -> None:
    quotation.delete()


# ===========================================================================
# PURCHASE ORDER SERVICES
# ===========================================================================

def get_all_purchase_orders() -> List[PurchaseOrder]:
    return PurchaseOrder.objects.all()

def get_purchase_order_with_items(po_id: int) -> PurchaseOrder:
    return PurchaseOrder.objects.prefetch_related('po_items').get(pk=po_id)

def create_purchase_order(data: Dict[str, Any]) -> PurchaseOrder:
    po_number = data.get('po_number')
    if PurchaseOrder.objects.filter(po_number__iexact=po_number).exists():
        raise ValueError(f"PO number '{po_number}' already exists.")
    items_data = data.pop('po_items', [])
    po = PurchaseOrder.objects.create(**data)
    for item_data in items_data:
        PurchaseOrderItem.objects.create(po=po, **item_data)
    return po

def update_purchase_order(po: PurchaseOrder, data: Dict[str, Any]) -> PurchaseOrder:
    for field, value in data.items():
        setattr(po, field, value)
    po.save()
    return po

def delete_purchase_order(po: PurchaseOrder) -> None:
    po.delete()


# ===========================================================================
# GRN SERVICES
# ===========================================================================

def get_all_grns() -> List[GRN]:
    return GRN.objects.all()

def get_grn_with_items(grn_id: int) -> GRN:
    return GRN.objects.prefetch_related('grn_items').get(pk=grn_id)

def create_grn(data: Dict[str, Any]) -> GRN:
    grn_number = data.get('grn_number')
    if GRN.objects.filter(grn_number__iexact=grn_number).exists():
        raise ValueError(f"GRN number '{grn_number}' already exists.")
    items_data = data.pop('grn_items', [])
    grn = GRN.objects.create(**data)
    for item_data in items_data:
        GRNItem.objects.create(grn=grn, **item_data)
    return grn

def update_grn(grn: GRN, data: Dict[str, Any]) -> GRN:
    for field, value in data.items():
        setattr(grn, field, value)
    grn.save()
    return grn

def delete_grn(grn: GRN) -> None:
    grn.delete()


# ===========================================================================
# PURCHASE INVOICE SERVICES
# ===========================================================================

def get_all_purchase_invoices() -> List[PurchaseInvoice]:
    return PurchaseInvoice.objects.all()

def get_purchase_invoice_with_items(invoice_id: int) -> PurchaseInvoice:
    return PurchaseInvoice.objects.prefetch_related('invoice_items').get(pk=invoice_id)

def create_purchase_invoice(data: Dict[str, Any]) -> PurchaseInvoice:
    invoice_number = data.get('invoice_number')
    if PurchaseInvoice.objects.filter(invoice_number__iexact=invoice_number).exists():
        raise ValueError(f"Invoice number '{invoice_number}' already exists.")
    items_data = data.pop('invoice_items', [])
    invoice = PurchaseInvoice.objects.create(**data)
    for item_data in items_data:
        PurchaseInvoiceItem.objects.create(invoice=invoice, **item_data)
    return invoice

def update_purchase_invoice(invoice: PurchaseInvoice, data: Dict[str, Any]) -> PurchaseInvoice:
    for field, value in data.items():
        setattr(invoice, field, value)
    invoice.save()
    return invoice

def delete_purchase_invoice(invoice: PurchaseInvoice) -> None:
    invoice.delete()


# ===========================================================================
# VENDOR PAYMENT SERVICES
# ===========================================================================

def get_all_vendor_payments() -> List[VendorPayment]:
    return VendorPayment.objects.all()

def create_vendor_payment(data: Dict[str, Any]) -> VendorPayment:
    payment_number = data.get('payment_number')
    if VendorPayment.objects.filter(payment_number__iexact=payment_number).exists():
        raise ValueError(f"Payment number '{payment_number}' already exists.")
    return VendorPayment.objects.create(**data)

def update_vendor_payment(payment: VendorPayment, data: Dict[str, Any]) -> VendorPayment:
    for field, value in data.items():
        setattr(payment, field, value)
    payment.save()
    return payment

def delete_vendor_payment(payment: VendorPayment) -> None:
    payment.delete()
