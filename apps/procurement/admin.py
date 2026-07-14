from django.contrib import admin
from .models import (
    VendorCategory, PaymentTerm, Vendor, VendorContact,
    PurchaseRequest, PurchaseRequestItem, RFQ, RFQVendor, RFQItem,
    Quotation, QuotationItem, PurchaseOrder, PurchaseOrderItem,
    GRN, GRNItem, PurchaseInvoice, PurchaseInvoiceItem, VendorPayment,
)


@admin.register(VendorCategory)
class VendorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_count', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(PaymentTerm)
class PaymentTermAdmin(admin.ModelAdmin):
    list_display = ('name', 'days', 'vendor_count', 'status', 'created_at')
    search_fields = ('name',)
    list_filter = ('status',)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category_name', 'city', 'country', 'rating', 'is_preferred', 'status', 'total_purchases', 'created_at')
    search_fields = ('code', 'name', 'gstin', 'pan', 'trn')
    list_filter = ('status', 'is_preferred', 'category')


@admin.register(VendorContact)
class VendorContactAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'designation', 'phone', 'email', 'is_primary', 'created_at')
    search_fields = ('name', 'vendor__name')
    list_filter = ('is_primary',)


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('pr_number', 'department', 'requested_by', 'date', 'priority', 'status', 'total_estimated_cost', 'created_at')
    search_fields = ('pr_number', 'department', 'requested_by')
    list_filter = ('status', 'priority')


@admin.register(PurchaseRequestItem)
class PurchaseRequestItemAdmin(admin.ModelAdmin):
    list_display = ('pr', 'item_name', 'sku', 'quantity', 'unit', 'required_date')
    search_fields = ('item_name', 'sku')


@admin.register(RFQ)
class RFQAdmin(admin.ModelAdmin):
    list_display = ('rfq_number', 'pr_number', 'date', 'due_date', 'status', 'created_by', 'created_at')
    search_fields = ('rfq_number', 'pr_number')
    list_filter = ('status',)


@admin.register(RFQVendor)
class RFQVendorAdmin(admin.ModelAdmin):
    list_display = ('rfq', 'vendor_name', 'status')
    search_fields = ('vendor_name',)
    list_filter = ('status',)


@admin.register(RFQItem)
class RFQItemAdmin(admin.ModelAdmin):
    list_display = ('rfq', 'item_name', 'sku', 'quantity', 'unit')
    search_fields = ('item_name', 'sku')


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quotation_number', 'rfq_number', 'vendor_name', 'date', 'valid_until', 'total_amount', 'status', 'created_at')
    search_fields = ('quotation_number', 'rfq_number', 'vendor_name')
    list_filter = ('status',)


@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'item_name', 'sku', 'quantity', 'unit_price', 'discount', 'tax', 'total')
    search_fields = ('item_name', 'sku')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor_name', 'vendor_city', 'total_amount', 'delivery_date', 'status', 'created_by', 'approved_by', 'created_at')
    search_fields = ('po_number', 'vendor_name')
    list_filter = ('status',)


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('po', 'item_name', 'sku', 'quantity', 'unit_price', 'discount', 'tax', 'total')
    search_fields = ('item_name', 'sku')


@admin.register(GRN)
class GRNAdmin(admin.ModelAdmin):
    list_display = ('grn_number', 'po_number', 'vendor_name', 'warehouse_name', 'total_received_value', 'status', 'received_by', 'verified_by', 'created_at')
    search_fields = ('grn_number', 'po_number')
    list_filter = ('status',)


@admin.register(GRNItem)
class GRNItemAdmin(admin.ModelAdmin):
    list_display = ('grn', 'item_name', 'sku', 'ordered_qty', 'received_qty', 'unit_price', 'total')
    search_fields = ('item_name', 'sku')


@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'po_number', 'vendor_name', 'invoice_date', 'due_date', 'total_amount', 'status', 'created_at')
    search_fields = ('invoice_number', 'po_number', 'vendor_name')
    list_filter = ('status',)


@admin.register(PurchaseInvoiceItem)
class PurchaseInvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'item_name', 'quantity', 'unit_price', 'tax', 'total')
    search_fields = ('item_name',)


@admin.register(VendorPayment)
class VendorPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'invoice_number', 'vendor_name', 'amount', 'payment_date', 'payment_method', 'status', 'created_at')
    search_fields = ('payment_number', 'invoice_number', 'vendor_name')
    list_filter = ('status', 'payment_method')
