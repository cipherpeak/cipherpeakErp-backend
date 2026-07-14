from rest_framework import serializers
from .models import (
    VendorCategory, PaymentTerm, Vendor, VendorContact,
    PurchaseRequest, PurchaseRequestItem, RFQ, RFQVendor, RFQItem,
    Quotation, QuotationItem, PurchaseOrder, PurchaseOrderItem,
    GRN, GRNItem, PurchaseInvoice, PurchaseInvoiceItem, VendorPayment,
)


# ===========================================================================
# VENDOR CATEGORY SERIALIZER
# ===========================================================================

class VendorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorCategory
        fields = '__all__'


# ===========================================================================
# PAYMENT TERMS SERIALIZER
# ===========================================================================

class PaymentTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTerm
        fields = '__all__'


# ===========================================================================
# VENDOR CONTACT SERIALIZER
# ===========================================================================

class VendorContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorContact
        fields = '__all__'


# ===========================================================================
# VENDOR SERIALIZER
# ===========================================================================

class VendorSerializer(serializers.ModelSerializer):
    contacts = VendorContactSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'


# ===========================================================================
# PURCHASE REQUEST ITEM SERIALIZER
# ===========================================================================

class PurchaseRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequestItem
        fields = '__all__'


# ===========================================================================
# PURCHASE REQUEST SERIALIZER
# ===========================================================================

class PurchaseRequestSerializer(serializers.ModelSerializer):
    pr_items = PurchaseRequestItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseRequest
        fields = '__all__'


# ===========================================================================
# RFQ VENDOR SERIALIZER
# ===========================================================================

class RFQVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQVendor
        fields = '__all__'


# ===========================================================================
# RFQ ITEM SERIALIZER
# ===========================================================================

class RFQItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem
        fields = '__all__'


# ===========================================================================
# RFQ SERIALIZER
# ===========================================================================

class RFQSerializer(serializers.ModelSerializer):
    rfq_vendors = RFQVendorSerializer(many=True, read_only=True)
    rfq_items = RFQItemSerializer(many=True, read_only=True)

    class Meta:
        model = RFQ
        fields = '__all__'


# ===========================================================================
# QUOTATION ITEM SERIALIZER
# ===========================================================================

class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = '__all__'


# ===========================================================================
# QUOTATION SERIALIZER
# ===========================================================================

class QuotationSerializer(serializers.ModelSerializer):
    quotation_items = QuotationItemSerializer(many=True, read_only=True)

    class Meta:
        model = Quotation
        fields = '__all__'


# ===========================================================================
# PURCHASE ORDER ITEM SERIALIZER
# ===========================================================================

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'


# ===========================================================================
# PURCHASE ORDER SERIALIZER
# ===========================================================================

class PurchaseOrderSerializer(serializers.ModelSerializer):
    po_items = PurchaseOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


# ===========================================================================
# GRN ITEM SERIALIZER
# ===========================================================================

class GRNItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GRNItem
        fields = '__all__'


# ===========================================================================
# GRN SERIALIZER
# ===========================================================================

class GRNSerializer(serializers.ModelSerializer):
    grn_items = GRNItemSerializer(many=True, read_only=True)

    class Meta:
        model = GRN
        fields = '__all__'


# ===========================================================================
# PURCHASE INVOICE ITEM SERIALIZER
# ===========================================================================

class PurchaseInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInvoiceItem
        fields = '__all__'


# ===========================================================================
# PURCHASE INVOICE SERIALIZER
# ===========================================================================

class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    invoice_items = PurchaseInvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseInvoice
        fields = '__all__'


# ===========================================================================
# VENDOR PAYMENT SERIALIZER
# ===========================================================================

class VendorPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPayment
        fields = '__all__'
